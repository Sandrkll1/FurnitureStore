// src/components/ProductCard.js
import React, { useContext, useState } from 'react';
import { Card, Button, InputGroup, FormControl, Carousel } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { FaShoppingCart } from 'react-icons/fa';
import { CartContext } from '../context/CartContext';
import {api, axiosInstance} from '../api/axiosConfig';

const ProductCard = ({ product }) => {
  const { cart, addToCart, removeFromCart } = useContext(CartContext);
  const [quantity, setQuantity] = useState(1);

  // Проверяем, есть ли продукт в корзине
  const inCart = cart && cart.items && cart.items.some(item => item.product_id === product.id);

  const handleAddToCart = () => {
    addToCart(product.id, quantity);
    setQuantity(1); // Сброс количества к 1 после добавления
  };

  const handleRemoveFromCart = () => {
    removeFromCart(product.id);
  };

  const getImageUrl = (imagePath) => {
    return `${axiosInstance.baseURL}/data/stream?image_path=${encodeURIComponent(imagePath)}`;
  };

  return (
    <Card className="h-100 shadow-sm">
      <Link to={`/products/${product.id}`}>
        {product.media && product.media.length > 0 ? (
          <Carousel indicators={false} controls={false} interval={3000}>
            {product.media.map((img, idx) => (
              <Carousel.Item key={idx}>
                <Card.Img
                  variant="top"
                  src={getImageUrl(img)}
                  alt={product.name}
                  style={{ height: '200px', objectFit: 'cover' }}
                />
              </Carousel.Item>
            ))}
          </Carousel>
        ) : (
          <Card.Img
            variant="top"
            src="placeholder-image-url"
            alt={product.name}
            style={{ height: '200px', objectFit: 'cover' }}
          />
        )}
      </Link>
      <Card.Body className="d-flex flex-column">
        <Card.Title>{product.name}</Card.Title>
        <Card.Text className="mt-auto">${product.price.toFixed(2)}</Card.Text>
        {inCart ? (
          <Button variant="danger" className="mb-2" onClick={handleRemoveFromCart}>
            Удалить из корзины
          </Button>
        ) : (
          <InputGroup className="mb-2">
            <FormControl
              type="number"
              min="1"
              value={quantity}
              onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
              aria-label="Количество"
            />
            <Button variant="primary" onClick={handleAddToCart}>
              <FaShoppingCart /> Добавить
            </Button>
          </InputGroup>
        )}
        <Button variant="outline-primary" as={Link} to={`/products/${product.id}`}>
          Подробнее
        </Button>
      </Card.Body>
    </Card>
  );
};

export default ProductCard;
