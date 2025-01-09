import React, { useEffect } from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import { FaUsers, FaHandshake, FaCogs } from 'react-icons/fa';
import AOS from 'aos';
import 'aos/dist/aos.css';

const About = () => {
  useEffect(() => {
    AOS.init({
      duration: 1000, // Продолжительность анимации в миллисекундах
      once: true, // Анимация происходит только один раз
    });
  }, []);

  return (
    <div>
      {/* 1. Hero Section */}
      <section id="about-hero" className="d-flex align-items-center" style={{ backgroundColor: '#f8f9fa', padding: '100px 0' }}>
        <Container>
          <Row className="align-items-center">
            <Col md={6} data-aos="fade-right">
              <h1>О нас</h1>
              <p>
                FurnitureStore - ваш надежный партнер в мире мебели. Мы предлагаем широкий ассортимент качественной и стильной мебели для дома и офиса.
              </p>
              <Button variant="primary" href="/catalog">
                Наш каталог
              </Button>
            </Col>
            <Col md={6} data-aos="fade-left">
              <img
                src="https://images.unsplash.com/photo-1524758631624-e2822e304c36?q=80&w=2970&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
                alt="О нас"
                className="img-fluid rounded shadow"
              />
            </Col>
          </Row>
        </Container>
      </section>

      {/* 2. Наша история */}
      <section id="our-story" className="py-5">
        <Container>
          <Row>
            <Col md={6} data-aos="fade-right">
              <img
                src="https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=800&q=80"
                alt="История компании"
                className="img-fluid rounded shadow"
              />
            </Col>
            <Col md={6} data-aos="fade-left">
              <h2>Наша история</h2>
              <p>
                Начиная с 2010 года, FurnitureStore стремится предоставлять клиентам лучшие мебельные решения. Мы начали как небольшой магазин, но благодаря высокому качеству продукции и отличному сервису, быстро выросли и стали одним из лидеров на рынке.
              </p>
              <p>
                Наша цель - создавать комфортные и стильные пространства, где каждый может найти что-то по своему вкусу и потребностям.
              </p>
            </Col>
          </Row>
        </Container>
      </section>

      {/* 3. Миссия и Видение */}
      <section id="mission-vision" className="bg-light py-5">
        <Container>
          <h2 className="text-center mb-4" data-aos="fade-up">Наша миссия и видение</h2>
          <Row>
            <Col md={4} className="mb-4" data-aos="fade-up">
              <Card className="text-center h-100">
                <Card.Body>
                  <FaHandshake size={50} color="#007bff" className="mb-3" />
                  <Card.Title>Миссия</Card.Title>
                  <Card.Text>
                    Наша миссия - предоставить качественную и доступную мебель, которая приносит радость и комфорт в дома наших клиентов.
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
            <Col md={4} className="mb-4" data-aos="fade-up" data-aos-delay="100">
              <Card className="text-center h-100">
                <Card.Body>
                  <FaCogs size={50} color="#007bff" className="mb-3" />
                  <Card.Title>Видение</Card.Title>
                  <Card.Text>
                    Мы стремимся стать ведущим мебельным брендом, известным своим инновационным дизайном и непревзойденным качеством.
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
            <Col md={4} className="mb-4" data-aos="fade-up" data-aos-delay="200">
              <Card className="text-center h-100">
                <Card.Body>
                  <FaUsers size={50} color="#007bff" className="mb-3" />
                  <Card.Title>Ценности</Card.Title>
                  <Card.Text>
                    Мы ценим честность, качество и заботу о клиентах. Каждое изделие создается с любовью и вниманием к деталям.
                  </Card.Text>
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Container>
      </section>

      {/* 4. Наша команда */}
      <section id="team" className="py-5">
        <Container>
          <h2 className="text-center mb-4" data-aos="fade-up">Наша команда</h2>
          <Row>
            {/* Пример карточек команды */}
            <Col md={4} className="mb-4" data-aos="zoom-in">
              <Card className="h-100 text-center">
                <Card.Img
                  variant="top"
                  src="https://i.pinimg.com/736x/10/25/a2/1025a2a1e64beeb40eda32791b0af9aa.jpg"
                  alt="Член команды"
                  className="rounded-circle mx-auto mt-3"
                  style={{ width: '150px', height: '150px', objectFit: 'cover' }}
                />
                <Card.Body>
                  <Card.Title>Иван Иванов</Card.Title>
                  <Card.Text>Генеральный директор</Card.Text>
                </Card.Body>
              </Card>
            </Col>
            <Col md={4} className="mb-4" data-aos="zoom-in" data-aos-delay="100">
              <Card className="h-100 text-center">
                <Card.Img
                  variant="top"
                  src="https://cs12.pikabu.ru/post_img/big/2022/12/10/1/1670627745123770458.jpg"
                  alt="Член команды"
                  className="rounded-circle mx-auto mt-3"
                  style={{ width: '150px', height: '150px', objectFit: 'cover' }}
                />
                <Card.Body>
                  <Card.Title>Изяслав Троицкий</Card.Title>
                  <Card.Text>Директор по продажам</Card.Text>
                </Card.Body>
              </Card>
            </Col>
            <Col md={4} className="mb-4" data-aos="zoom-in" data-aos-delay="200">
              <Card className="h-100 text-center">
                <Card.Img
                  variant="top"
                  src="https://assets.gq.ru/photos/5d9f60b9590ee50009c98014/master/w_1600%2Cc_limit/05.jpg"
                  alt="Член команды"
                  className="rounded-circle mx-auto mt-3"
                  style={{ width: '150px', height: '150px', objectFit: 'cover' }}
                />
                <Card.Body>
                  <Card.Title>Алексей Петров</Card.Title>
                  <Card.Text>Главный дизайнер</Card.Text>
                </Card.Body>
              </Card>
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
                      "FurnitureStore превзошел все наши ожидания. Мебель высокого качества и отличное обслуживание клиентов."
                    </p>
                    <footer className="blockquote-footer">Елена Кузнецова</footer>
                  </blockquote>
                </Card.Body>
              </Card>
            </Col>
            <Col md={8} data-aos="fade-up" data-aos-delay="200">
              <Card className="mb-4">
                <Card.Body>
                  <blockquote className="blockquote mb-0">
                    <p>
                      "Купили диван и кровать от FurnitureStore. Очень довольны качеством и дизайном. Рекомендую всем!"
                    </p>
                    <footer className="blockquote-footer">Олег Николаев</footer>
                  </blockquote>
                </Card.Body>
              </Card>
            </Col>
            <Col md={8} data-aos="fade-up" data-aos-delay="300">
              <Card className="mb-4">
                <Card.Body>
                  <blockquote className="blockquote mb-0">
                    <p>
                      "Отличный выбор мебели и внимательный персонал. Спасибо за помощь в выборе идеального стола для офиса."
                    </p>
                    <footer className="blockquote-footer">Ирина Васильева</footer>
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

export default About;
