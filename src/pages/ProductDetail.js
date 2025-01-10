import React, { useEffect, useState, useContext } from 'react';
import { Container, Row, Col, Image, Spinner, Alert, Button, InputGroup, FormControl } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import axios from '../api/axiosConfig';
import { FaShoppingCart } from 'react-icons/fa';
import { CartContext } from '../context/CartContext';
import { AuthContext } from '../context/AuthContext';

const ProductDetail = () => {
  const { id } = useParams();
  const { user } = useContext(AuthContext);
  const { cart, addToCart, removeFromCart } = useContext(CartContext);

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [quantity, setQuantity] = useState(1);

  const inCart = cart && cart.items && cart.items.some(item => item.product_id === parseInt(id, 10));

  useEffect(() => {
    fetchProduct();
  }, [id]);

  const fetchProduct = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(`/products/${id}`);
      if (!response.data || response.status !== 200) {
        throw new Error('Продукт не найден');
      }
      setProduct(response.data);
    } catch (err) {
      console.error('Ошибка при загрузке продукта:', err);
      setError('Не удалось загрузить продукт. Пожалуйста, попробуйте позже.');
    } finally {
      setLoading(false);
    }
  };

  const getImageUrl = (imagePath) => {
    return `https://course.excellentjewellery.ru/furniture/api/data/stream?image_path=${imagePath}`;
  };

  const handleAddToCart = () => {
    addToCart(product.id, quantity);
    setQuantity(1);
  };

  const handleRemoveFromCart = () => {
    removeFromCart(product.id);
  };

  if (loading) {
    return (
      <Container className="text-center my-5">
        <Spinner animation="border" role="status" />
        <span className="ms-2">Загрузка продукта...</span>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="my-5">
        <Alert variant="danger" className="text-center">
          {error}
        </Alert>
      </Container>
    );
  }

  if (!product) {
    return (
      <Container className="my-5">
        <Alert variant="warning" className="text-center">
          Продукт не найден.
        </Alert>
      </Container>
    );
  }

  return (
    <div>
      <section id="product-hero" className="d-flex align-items-center" style={{ backgroundColor: '#f8f9fa', padding: '80px 0' }}>
        <Container>
          <Row>
            <Col md={12}>
              <h1 className="text-center">{product.name}</h1>
            </Col>
          </Row>
        </Container>
      </section>

      <section id="product-details" className="py-5">
        <Container>
          <Row>
            <Col md={6}>
              {product.media && product.media.length > 0 ? (
                <Image
                  src={getImageUrl(product.media[0])}
                  alt={product.name}
                  fluid
                  rounded
                  shadow
                />
              ) : (
                <Image
                  src="placeholder-image-url"
                  alt="Нет изображения"
                  fluid
                  rounded
                  shadow
                />
              )}
            </Col>
            <Col md={6}>
              <h2>{product.name}</h2>
              <h4 className="text-primary">${product.price.toFixed(2)}</h4>
              <p className="text-muted">{product.category}</p>
              <p>{product.description}</p>

              {inCart ? (
                <Button variant="danger" className="mb-3" onClick={handleRemoveFromCart}>
                  Удалить из корзины
                </Button>
              ) : (
                <InputGroup className="mb-3">
                  <FormControl
                    type="number"
                    min="1"
                    value={quantity}
                    onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value, 10) || 1))}
                  />
                  <Button variant="success" onClick={handleAddToCart}>
                    <FaShoppingCart className="me-2" /> Добавить в корзину
                  </Button>
                </InputGroup>
              )}

              {!user && (
                <p className="mt-2 text-danger">
                  Пожалуйста, <a href="/login">войдите</a>, чтобы добавлять товары в корзину.
                </p>
              )}
            </Col>
          </Row>
        </Container>
      </section>
    </div>
  );
};

export default ProductDetail;
