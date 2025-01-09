import React, { useContext, useState, useEffect } from 'react';
import { Container, Table, Form, Button, Alert, Spinner } from 'react-bootstrap';
import { CartContext } from '../context/CartContext';
import axios from '../api/axiosConfig';
import { useNavigate } from 'react-router-dom';

const Checkout = () => {
  const { cart, fetchCart, clearCart } = useContext(CartContext); // Добавлена очистка корзины
  const [email, setEmail] = useState('');
  const [address, setAddress] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCart();
  }, []);

  // Пересчет общей суммы корзины
  const calculateTotalPrice = () => {
    return cart.items.reduce((total, item) => total + item.price * item.quantity, 0);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage(null);
    setError(null);

    try {
      // Отправка данных на сервер
      const response = await axios.post('/cart/order', {
        delivery_address: address,
        email,
      });

      if (response.status === 200) {
        setMessage('Ваш заказ успешно оформлен! С вами скоро свяжется наш менеджер.');
        clearCart(); // Очистка корзины
        setEmail('');
        setAddress('');
        setTimeout(() => navigate('/'), 3000); // Переход на главную через 3 секунды
      }
    } catch (err) {
      console.error('Ошибка при оформлении заказа:', err);
      setError('Не удалось оформить заказ. Попробуйте снова.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!cart || !cart.items || cart.items.length === 0) {
    return (
      <Container className="my-5">
        <Alert variant="info" className="text-center">
          Ваша корзина пуста.{' '}
          <Button variant="link" onClick={() => navigate('/catalog')}>
            Перейти в каталог
          </Button>
        </Alert>
      </Container>
    );
  }

  return (
    <Container className="my-5" style={{ maxWidth: '700px' }}>
      <h2 className="text-center mb-4">Оформление заказа</h2>
      {message && <Alert variant="success">{message}</Alert>}
      {error && <Alert variant="danger">{error}</Alert>}

      {/* Список товаров */}
      <h4 className="mb-3">Ваши товары</h4>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>Товар</th>
            <th>Количество</th>
            <th>Цена</th>
            <th>Итого</th>
          </tr>
        </thead>
        <tbody>
          {cart.items.map((item) => (
            <tr key={item.product_id}>
              <td>{item.product_name}</td>
              <td>{item.quantity}</td>
              <td>${item.price.toFixed(2)}</td>
              <td>${(item.price * item.quantity).toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </Table>

      <h5 className="text-end">Общая сумма: ${calculateTotalPrice().toFixed(2)}</h5>

      {/* Форма оформления заказа */}
      <Form onSubmit={handleSubmit} className="mt-4">
        <Form.Group className="mb-3" controlId="email">
          <Form.Label>Ваш email</Form.Label>
          <Form.Control
            type="email"
            placeholder="Введите ваш email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </Form.Group>
        <Form.Group className="mb-3" controlId="address">
          <Form.Label>Адрес доставки</Form.Label>
          <Form.Control
            type="text"
            placeholder="Введите ваш адрес доставки"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            required
          />
        </Form.Group>
        <Button variant="primary" type="submit" className="w-100" disabled={isSubmitting}>
          {isSubmitting ? <Spinner animation="border" size="sm" /> : 'Подтвердить заказ'}
        </Button>
      </Form>
    </Container>
  );
};

export default Checkout;
