// src/pages/Home.js

import React, { useEffect } from 'react';
import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { FaChair, FaCouch, FaBed } from 'react-icons/fa';
import AOS from 'aos';
import 'aos/dist/aos.css';

const Home = () => {
  useEffect(() => {
    AOS.init({
      duration: 1000, // Продолжительность анимации в миллисекундах
      once: true, // Анимация происходит только один раз
    });
  }, []);

  return (
    <div>
      {/* 1. Hero Section */}
      <section id="hero" className="d-flex align-items-center">
        <Container className="content">
          <Row>
            <Col md={6} data-aos="fade-right">
              <h1>Добро пожаловать в FurnitureStore</h1>
              <p>Лучшие мебельные решения для вашего дома и офиса. Высокое качество, стильный дизайн и доступные цены.</p>
              <Button as={Link} to="/catalog" variant="primary" size="lg">
                Посмотреть каталог
              </Button>
            </Col>
            <Col md={6} data-aos="fade-left">
              <img
                src="https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=800&q=80"
                alt="Мебель"
                className="img-fluid rounded shadow"
              />
            </Col>
          </Row>
        </Container>
      </section>

      {/* 2. Новые поступления */}
      <section id="new-arrivals" className="py-5">
        <Container>
          <h2 className="text-center mb-4" data-aos="fade-up">Новые поступления</h2>
          <Row>
            <Col md={4} className="mb-4" data-aos="zoom-in">
              <Card className="h-100">
                <Card.Img
                  variant="top"
                  src="https://images.unsplash.com/photo-1625461291092-13d0c45608b3?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fG1vZGVybiUyMGRlc2t8ZW58MHx8MHx8fDA%3D"
                  alt="Современный стол"
                  style={{
                    height: '250px',
                    width: '100%',
                    objectFit: 'cover',
                  }}
                />
                <Card.Body className="d-flex flex-column">
                  <Card.Title>Современный стол</Card.Title>
                  <Card.Text>Идеально подходит для любой кухни или офиса. Стильный дизайн и прочные материалы.</Card.Text>
                  <Button variant="primary" as={Link} to="/catalog">
                    Купить
                  </Button>
                </Card.Body>
              </Card>
            </Col>
            <Col md={4} className="mb-4" data-aos="zoom-in" data-aos-delay="100">
              <Card className="h-100">
                <Card.Img
                  variant="top"
                  src="https://images.unsplash.com/photo-1519947486511-46149fa0a254?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8Y2hhaXJ8ZW58MHx8MHx8fDA%3D"
                  alt="Эргономичное кресло"
                  style={{
                    height: '250px',
                    width: '100%',
                    objectFit: 'cover',
                  }}
                />
                <Card.Body className="d-flex flex-column">
                  <Card.Title>Эргономичное кресло</Card.Title>
                  <Card.Text>Максимальный комфорт для долгих часов работы. Регулируемая спинка и подлокотники.</Card.Text>
                  <Button variant="primary" as={Link} to="/catalog">
                    Купить
                  </Button>
                </Card.Body>
              </Card>
            </Col>
            <Col md={4} className="mb-4" data-aos="zoom-in" data-aos-delay="200">
              <Card className="h-100">
                <Card.Img
                  variant="top"
                  src="https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGJlZHxlbnwwfHwwfHx8MA%3D%3D"
                  alt="Комфортная кровать"
                  style={{
                    height: '250px',
                    width: '100%',
                    objectFit: 'cover',
                  }}
                />
                <Card.Body className="d-flex flex-column">
                  <Card.Title>Комфортная кровать</Card.Title>
                  <Card.Text>Превосходное качество и стильный дизайн. Удобный матрас и надежная конструкция.</Card.Text>
                  <Button variant="primary" as={Link} to="/catalog">
                    Купить
                  </Button>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>


      {/* 3. Популярные категории */}
      <section id="categories" className="bg-light py-5">
        <Container>
          <h2 className="text-center mb-4" data-aos="fade-up">Популярные категории</h2>
          <Row>
            <Col md={4} className="mb-4" data-aos="fade-right">
              <Card className="h-100 text-center">
                <Card.Body>
                  <FaCouch size={50} className="mb-3" color="#007bff" />
                  <Card.Title>Диваны</Card.Title>
                  <Card.Text>Широкий выбор диванов для любой комнаты. Комфорт и стиль в одном флаконе.</Card.Text>
                  <Button variant="secondary" as={Link} to="/catalog?category=divans">
                    Смотреть
                  </Button>
                </Card.Body>
              </Card>
            </Col>
            <Col md={4} className="mb-4" data-aos="fade-up">
              <Card className="h-100 text-center">
                <Card.Body>
                  <FaBed size={50} className="mb-3" color="#007bff" />
                  <Card.Title>Кровати</Card.Title>
                  <Card.Text>Комфортные и стильные кровати для вашего сна. Выбор размеров и материалов.</Card.Text>
                  <Button variant="secondary" as={Link} to="/catalog?category=krovaty">
                    Смотреть
                  </Button>
                </Card.Body>
              </Card>
            </Col>
            <Col md={4} className="mb-4" data-aos="fade-left">
              <Card className="h-100 text-center">
                <Card.Body>
                  <FaChair size={50} className="mb-3" color="#007bff" />
                  <Card.Title>Стулья</Card.Title>
                  <Card.Text>Разнообразие стульев для дома и офиса. Эргономика и дизайн.</Card.Text>
                  <Button variant="secondary" as={Link} to="/catalog?category=stulya">
                    Смотреть
                  </Button>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>

      {/* 4. Почему выбирают нас */}
      <section id="why-us" className="py-5">
        <Container>
          <h2 className="text-center mb-4" data-aos="fade-up">Почему выбирают нас</h2>
          <Row>
            <Col md={4} className="mb-4" data-aos="fade-right">
              <div className="feature">
                <i className="bi bi-truck" style={{ fontSize: '3rem', color: '#007bff', marginBottom: '15px' }}></i>
                <h5>Быстрая доставка</h5>
                <p>Мы обеспечиваем быструю и надежную доставку вашей мебели прямо к двери.</p>
              </div>
            </Col>
            <Col md={4} className="mb-4" data-aos="fade-up">
              <div className="feature">
                <i className="bi bi-award" style={{ fontSize: '3rem', color: '#007bff', marginBottom: '15px' }}></i>
                <h5>Высокое качество</h5>
                <p>Наша мебель изготовлена из высококачественных материалов, гарантируя долговечность и комфорт.</p>
              </div>
            </Col>
            <Col md={4} className="mb-4" data-aos="fade-left">
              <div className="feature">
                <i className="bi bi-headset" style={{ fontSize: '3rem', color: '#007bff', marginBottom: '15px' }}></i>
                <h5>Отличная поддержка</h5>
                <p>Наша служба поддержки всегда готова помочь вам с любыми вопросами и проблемами.</p>
              </div>
            </Col>
          </Row>
        </Container>
      </section>

      {/* 5. Отзывы клиентов */}
      <section id="testimonials" className="bg-light py-5">
        <Container>
          <h2 className="text-center mb-4" data-aos="fade-up">Отзывы клиентов</h2>
          <Row className="justify-content-center">
            <Col md={8} data-aos="fade-up" data-aos-delay="100">
              <Card className="mb-4">
                <Card.Body>
                  <blockquote className="blockquote mb-0">
                    <p>
                      "Прекрасный сервис и отличная мебель! Доставка была быстрой, а качество превзошло все ожидания."
                    </p>
                    <footer className="blockquote-footer">Анна Иванова</footer>
                  </blockquote>
                </Card.Body>
              </Card>
            </Col>
            <Col md={8} data-aos="fade-up" data-aos-delay="200">
              <Card className="mb-4">
                <Card.Body>
                  <blockquote className="blockquote mb-0">
                    <p>
                      "Очень довольны покупкой. Диван выглядит стильно и удобно, идеально вписался в нашу гостиную."
                    </p>
                    <footer className="blockquote-footer">Сергей Петров</footer>
                  </blockquote>
                </Card.Body>
              </Card>
            </Col>
            <Col md={8} data-aos="fade-up" data-aos-delay="300">
              <Card className="mb-4">
                <Card.Body>
                  <blockquote className="blockquote mb-0">
                    <p>
                      "Отличное качество и отличный сервис. Рекомендую всем, кто ищет качественную мебель."
                    </p>
                    <footer className="blockquote-footer">Мария Смирнова</footer>
                  </blockquote>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>
    </div>
  );
};

export default Home;
