// src/components/Navbar.js

import React, { useContext } from 'react';
import { Navbar, Nav, Container, NavDropdown, Spinner } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';

const NavigationBar = () => {
  const { user, logout, loading } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <Navbar bg="light" expand="lg" sticky="top">
      <Container>
        <Navbar.Brand as={Link} to="/">FurnitureStore</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">Главная</Nav.Link>
            <Nav.Link as={Link} to="/about">О нас</Nav.Link>
            <Nav.Link as={Link} to="/catalog">Каталог</Nav.Link>
          </Nav>
          <Nav>
            {loading ? (
              <Spinner animation="border" size="sm" />
            ) : user ? (
              <>
                <Nav.Link as={Link} to="/cart">Корзина</Nav.Link>
                <NavDropdown title={user.name} id="basic-nav-dropdown">
                  <NavDropdown.Item as={Link} to="/profile">Профиль</NavDropdown.Item>
                  <NavDropdown.Divider />
                  <NavDropdown.Item onClick={handleLogout}>Выйти</NavDropdown.Item>
                </NavDropdown>
              </>
            ) : (
              <>
                <Nav.Link as={Link} to="/login">Вход</Nav.Link>
                <Nav.Link as={Link} to="/register">Регистрация</Nav.Link>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavigationBar;
