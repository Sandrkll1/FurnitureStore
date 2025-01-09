// src/pages/Register.js
import React, { useState, useContext } from 'react';
import { Container, Row, Col, Form, Button, Alert } from 'react-bootstrap';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const { register } = useContext(AuthContext);
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    if (password.length < 8) {
      setError('Пароль должен быть не менее 8 символов.');
      setLoading(false);
      return;
    }

    const result = await register(name, email, password);
    if (result.success) {
      navigate('/catalog');
    } else {
      setError(result.message);
    }
    setLoading(false);
  };

  return (
    <Container className="my-5">
      <Row className="justify-content-center">
        <Col md={6}>
          <h2 className="text-center mb-4">Регистрация</h2>
          {error && <Alert variant="danger">{error}</Alert>}
          <Form onSubmit={handleRegister}>
            <Form.Group controlId="registerName" className="mb-3">
              <Form.Label>Имя</Form.Label>
              <Form.Control
                type="text"
                placeholder="Введите имя"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="registerEmail" className="mb-3">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                placeholder="Введите email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </Form.Group>
            <Form.Group controlId="registerPassword" className="mb-3">
              <Form.Label>Пароль</Form.Label>
              <Form.Control
                type="password"
                placeholder="Введите пароль"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </Form.Group>
            <Button variant="primary" type="submit" disabled={loading} className="w-100">
              {loading ? 'Регистрация...' : 'Зарегистрироваться'}
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default Register;
