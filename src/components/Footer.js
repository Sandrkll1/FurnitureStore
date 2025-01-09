// src/components/Footer.js

import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { FaFacebookF, FaInstagram, FaTwitter } from 'react-icons/fa';

const Footer = () => {
  return (
    <footer className="bg-dark text-white py-4">
      <Container>
        <Row>
          <Col md={4}>
            <h5>FurnitureStore</h5>
            <p>Лучшие мебельные решения для вашего дома и офиса.</p>
          </Col>
          <Col md={4}>
            <h5>Контакты</h5>
            <p>Email: support@furniturestore.com</p>
            <p>Телефон: +375 (123) 456-78-90</p>
            <p>Адрес: г. Минск, ул. Примерная, д.1</p>
          </Col>
          <Col md={4}>
            <h5>Следите за нами</h5>
            <a href="https://facebook.com" className="text-white me-3">
              <FaFacebookF size={24} />
            </a>
            <a href="https://instagram.com" className="text-white me-3">
              <FaInstagram size={24} />
            </a>
            <a href="https://twitter.com" className="text-white">
              <FaTwitter size={24} />
            </a>
          </Col>
        </Row>
        <Row className="mt-3">
          <Col className="text-center">
            <small>&copy; {new Date().getFullYear()} FurnitureStore. Все права защищены.</small>
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;
