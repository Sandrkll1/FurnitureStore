import React, { useContext, useEffect, useState } from 'react';
import { Container, Table, Button, Alert, Spinner, InputGroup, FormControl } from 'react-bootstrap';
import { CartContext } from '../context/CartContext';
import { useNavigate } from 'react-router-dom';

const Cart = () => {
  const { cart, loading, fetchCart, removeFromCart, updateQuantity } = useContext(CartContext);
  const [quantities, setQuantities] = useState({});
  const [updating, setUpdating] = useState(false);
  const navigate = useNavigate(); // Для навигации между страницами

  useEffect(() => {
    fetchCart();
  }, []);

  useEffect(() => {
    if (cart && cart.items) {
      const initialQuantities = {};
      cart.items.forEach((item) => {
        initialQuantities[item.product_id] = item.quantity;
      });
      setQuantities(initialQuantities);
    }
  }, [cart]);

  const handleQuantityChange = (productId, value) => {
    const newQuantity = Math.max(1, parseInt(value, 10) || 1);
    setQuantities((prev) => ({
      ...prev,
      [productId]: newQuantity,
    }));
  };

  const handleUpdateQuantity = async (productId) => {
    const quantity = quantities[productId];
    if (quantity > 0) {
      setUpdating(true);
      await updateQuantity(productId, quantity);
      await fetchCart();
      setUpdating(false);
    }
  };

  const handleRemoveFromCart = async (productId) => {
    setUpdating(true);
    await removeFromCart(productId);
    await fetchCart();
    setUpdating(false);
  };

  const handleCheckout = () => {
    navigate('/checkout'); // Переход на страницу оформления заказа
  };

  // Пересчет общей суммы корзины
  const calculateTotalPrice = () => {
    return cart.items.reduce((total, item) => {
      const quantity = quantities[item.product_id] || item.quantity;
      return total + item.price * quantity;
    }, 0);
  };

  if (loading || updating) {
    return (
      <Container className="text-center my-5">
        <Spinner animation="border" role="status" />
        <span className="ms-2">Загрузка корзины...</span>
      </Container>
    );
  }

  if (!cart || !cart.items || cart.items.length === 0) {
    return (
      <Container className="my-5">
        <Alert variant="info" className="text-center">
          Ваша корзина пуста.
        </Alert>
      </Container>
    );
  }

  return (
    <Container className="my-5">
      <h2 className="mb-4">Ваша корзина</h2>
      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>Товар</th>
            <th>Цена</th>
            <th>Количество</th>
            <th>Итого</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          {cart.items.map((item) => (
            <tr key={item.product_id}>
              <td>{item.product_name}</td>
              <td>${item.price.toFixed(2)}</td>
              <td>
                <InputGroup>
                  <FormControl
                    type="number"
                    min="1"
                    value={quantities[item.product_id] || item.quantity}
                    onChange={(e) => handleQuantityChange(item.product_id, e.target.value)}
                  />
                  <Button
                    variant="outline-secondary"
                    onClick={() => handleUpdateQuantity(item.product_id)}
                    disabled={updating}
                  >
                    Обновить
                  </Button>
                </InputGroup>
              </td>
              <td>${(item.price * (quantities[item.product_id] || item.quantity)).toFixed(2)}</td>
              <td>
                <Button
                  variant="danger"
                  size="sm"
                  onClick={() => handleRemoveFromCart(item.product_id)}
                  disabled={updating}
                >
                  Удалить
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
      {/* Отображаем пересчитанную сумму */}
      <h4 className="text-end">
        Общая сумма: ${calculateTotalPrice().toFixed(2)}
      </h4>
      <div className="text-end">
        <Button variant="success" onClick={handleCheckout}>
          Оформить заказ
        </Button>
      </div>
    </Container>
  );
};

export default Cart;
