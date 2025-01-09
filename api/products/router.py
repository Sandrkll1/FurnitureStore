import json
import os
from typing import Any, Optional

from fastapi import (APIRouter, Depends, File, Form, HTTPException, UploadFile,
                     status)
from fastapi_cache.decorator import cache

import config
from api.dependencies import (get_current_admin, get_current_user,
                              get_service_manager)
from api.products.schemas import (ProductCategoryCreate,
                                  ProductCreate,
                                  ProductResponse,
                                  ProductUpdate, ProductCategoryResponse)
from database.models.user import User
from database.service_manager import ServiceManager
from utils import save_files

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/category", response_model=list[ProductCategoryResponse])
# @cache(expire=300)
async def get_categories(
        user: User = Depends(get_current_user),
        manager: ServiceManager = Depends(get_service_manager),
):
    return [
        ProductCategoryResponse.model_validate(category, from_attributes=True)
        for category in await manager.product_category.get_all()
    ]


@router.get("/category/{category_id}", response_model=list[ProductResponse])
# @cache(expire=300)
async def get_products_by_category(
        category_id: int = None,
        limit: int = 50,
        offset: int = 0,
        search: Optional[str] = None,
        user: User = Depends(get_current_user),
        manager: ServiceManager = Depends(get_service_manager),
):
    products = await manager.product.get_products(
        category_id=category_id,
        limit=limit,
        offset=offset,
        search=search
    )

    return [
        ProductResponse.model_validate(product, from_attributes=True)
        for product in products
    ]


@router.get("/new", response_model=list[ProductResponse])
@cache(expire=120)
async def get_new_products(
    limit: int = 1000,
    offset: int = 0,
    user: User = Depends(get_current_user),
    manager: ServiceManager = Depends(get_service_manager)
):
    return [
        ProductResponse.model_validate(product, from_attributes=True)
        for product in await manager.product.get_new_products(limit=limit, offset=offset)
    ]


# @router.get("/personal-offers", response_model=list[ProductResponse])
# @cache(expire=120)
# async def get_personal_offers(
#         limit: int = 10,
#         user: User = Depends(get_current_user),
#         manager: ServiceManager = Depends(get_service_manager),
# ):
#     orders = await manager.order.get_orders_by_user_id(user.user_id, status=OrderStatus.COMPLETED.value)
#     if orders:
#         recommended_products = await controller.get_recommendations_based_on_purchases(user, orders, manager, limit)
#     else:
#         recommended_products = await controller.get_recommendations_based_on_test_answer(user, manager, limit)
#
#     return await controller.get_products_with_discounts(user, recommended_products, manager)


@router.get("/{product_id}", response_model=ProductResponse)
@cache(expire=300)
async def get_product_detail(
        product_id: int,
        user: User = Depends(get_current_user),
        manager: ServiceManager = Depends(get_service_manager),
):
    product = await manager.product.get_product_detail(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return ProductResponse.model_validate(product, from_attributes=True)


@router.post("/categories", status_code=status.HTTP_201_CREATED)
async def create_category(
        category_data: str = Form(...),
        image: UploadFile = File(None),
        admin: Any = Depends(get_current_admin),
        manager: ServiceManager = Depends(get_service_manager),
):
    category_data = ProductCategoryCreate(**json.loads(category_data))

    product_category = await manager.product_category.get_by_name(category_data.name)
    if product_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists"
        )

    if image:
        category_data.image = await save_files.save_image(image, config.MEDIA_PATH)

    await manager.product_category.create(**category_data.model_dump(exclude={"translations"}))
    return {"message": "Category created successfully"}


@router.put("/categories", status_code=status.HTTP_200_OK)
async def update_category(
        category_data: str = Form(...),
        image: UploadFile = File(None),
        admin: User = Depends(get_current_admin),
        manager: ServiceManager = Depends(get_service_manager)
):
    category_data = ProductCategoryResponse(**json.loads(category_data))

    product_category = await manager.product_category.get(category_data.id)
    if not product_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    if image:
        os.remove(os.path.join(config.MEDIA_PATH, category_data.image))
        category_data.image = await save_files.save_image(image, config.MEDIA_PATH)

    await manager.product_category.update(product_category.id, category_data.model_dump(exclude={"translations"}))
    return {"message": "Category updated successfully"}


@router.delete("/categories/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(
        category_id: int,
        admin: User = Depends(get_current_admin),
        manager: ServiceManager = Depends(get_service_manager),
):
    success = await manager.product_category.delete(category_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return {"message": "Category deleted successfully"}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
        product_data: str = Form(...),
        files: list[UploadFile] = File([]),
        admin: User = Depends(get_current_admin),
        manager: ServiceManager = Depends(get_service_manager)
):
    product_data = ProductCreate(**json.loads(product_data))

    files = await save_files.save_media_files(files, config.MEDIA_PATH)

    await manager.product.create_product(
        media=files,
        **product_data.model_dump(exclude={"media", "translations"})
    )
    return {"message": "Product created successfully"}


@router.put("/", status_code=status.HTTP_200_OK)
async def update_product(
        product_data: str = Form(...),
        files: list[UploadFile] = File(None),
        admin: User = Depends(get_current_admin),
        manager: ServiceManager = Depends(get_service_manager)
):
    product_data = ProductUpdate(**json.loads(product_data))

    product = await manager.product.get(product_data.id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    media_files = product_data.media or []
    if files:
        new_media_files = await save_files.save_media_files(files, config.MEDIA_PATH)
        media_files.extend(new_media_files)

    await manager.product.update_product(
        media=media_files,
        **product_data.model_dump(exclude={"media", "translations"}, exclude_none=True)
    )
    return {"message": "Product updated successfully"}


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(
        product_id: int,
        admin: User = Depends(get_current_admin),
        manager: ServiceManager = Depends(get_service_manager)
):
    await manager.product.update(product_id, deleted=True)
    return {"message": "Product deleted successfully"}
