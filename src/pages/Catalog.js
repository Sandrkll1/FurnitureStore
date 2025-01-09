// src/pages/Catalog.js
import React, { useEffect, useState, useContext } from 'react';
import { Container, Row, Col, Spinner, Alert, Form, Button } from 'react-bootstrap';
import ProductCard from '../components/ProductCard';
import axios from '../api/axiosConfig';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { AuthContext } from '../context/AuthContext';

const Catalog = () => {
  const { user } = useContext(AuthContext);

  const [categories, setCategories] = useState([]);
  const [selectedCategoryId, setSelectedCategoryId] = useState(null);
  const [products, setProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortType, setSortType] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Получение списка категорий
  const fetchCategories = async () => {
    try {
      const response = await axios.get('/products/category');
      setCategories(response.data);
      // Если нужно сразу выбрать первую категорию
      if (response.data.length > 0) {
        setSelectedCategoryId(response.data[0].id);
      }
    } catch (err) {
      console.error('Ошибка при загрузке категорий:', err);
    }
  };

  // Получение продуктов по категории с учётом поискового запроса
  const fetchProducts = async (categoryId, search = '') => {
    if (!categoryId) return;
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(`/products/category/${categoryId}`, {
        params: { search },
      });
      let data = response.data;
      
      // Сортировка на клиенте
      if (sortType === 'price_asc') {
        data = data.sort((a, b) => a.price - b.price);
      } else if (sortType === 'price_desc') {
        data = data.sort((a, b) => b.price - a.price);
      } else if (sortType === 'name_asc') {
        data = data.sort((a, b) => a.name.localeCompare(b.name));
      } else if (sortType === 'name_desc') {
        data = data.sort((a, b) => b.name.localeCompare(a.name));
      }

      setProducts(data);
    } catch (err) {
      console.error('Ошибка при загрузке продуктов:', err);
      setError('Не удалось загрузить продукты. Пожалуйста, попробуйте позже.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    AOS.init({ duration: 1000, once: true });
    fetchCategories();
  }, []);

  useEffect(() => {
    if (selectedCategoryId) {
      fetchProducts(selectedCategoryId, searchTerm);
    }
  }, [selectedCategoryId, searchTerm, sortType]);

  const handleCategoryChange = (e) => {
    const categoryId = e.target.value;
    setSelectedCategoryId(categoryId);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchProducts(selectedCategoryId, searchTerm);
  };

  return (
    <div>
      <section
        id="catalog-hero"
        className="d-flex align-items-center"
        style={{ backgroundColor: '#f8f9fa', padding: '80px 0' }}
      >
        <Container>
          <Row>
            <Col md={12} data-aos="fade-up">
              <h1 className="text-center">Каталог</h1>
              <p className="text-center">Выберите из широкого ассортимента качественной и стильной мебели.</p>
            </Col>
          </Row>
        </Container>
      </section>

      <section id="filters" className="py-4">
        <Container>
          <Row className="justify-content-center mb-3">
            <Col md={4} data-aos="fade-up">
              <Form.Group controlId="categorySelect">
                <Form.Label>Категория</Form.Label>
                <Form.Control as="select" value={selectedCategoryId || ''} onChange={handleCategoryChange}>
                  {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>
                      {cat.name}
                    </option>
                  ))}
                </Form.Control>
              </Form.Group>
            </Col>

            <Col md={4} data-aos="fade-up">
              <Form.Group controlId="sortSelect">
                <Form.Label>Сортировка</Form.Label>
                <Form.Control
                  as="select"
                  value={sortType}
                  onChange={(e) => setSortType(e.target.value)}
                >
                  <option value="">Без сортировки</option>
                  <option value="price_asc">Цена по возрастанию</option>
                  <option value="price_desc">Цена по убыванию</option>
                  <option value="name_asc">Название A-Z</option>
                  <option value="name_desc">Название Z-A</option>
                </Form.Control>
              </Form.Group>
            </Col>
          </Row>

          <Row className="justify-content-center">
            <Col md={8} data-aos="fade-up">
              <Form onSubmit={handleSearchSubmit} className="d-flex">
                <Form.Control
                  type="text"
                  placeholder="Поиск по названию..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <Button type="submit" variant="primary" className="ms-2">
                  Поиск
                </Button>
              </Form>
            </Col>
          </Row>
        </Container>
      </section>

      <section id="product-list" className="py-5">
        <Container>
          {loading ? (
            <div className="text-center">
              <Spinner animation="border" role="status" />
              <span className="ms-2">Загрузка продуктов...</span>
            </div>
          ) : error ? (
            <Alert variant="danger" className="text-center">
              {error}
            </Alert>
          ) : products.length === 0 ? (
            <Alert variant="info" className="text-center">
              Нет доступных продуктов.
            </Alert>
          ) : (
            <Row>
              {products.map((product) => (
                <Col md={4} lg={3} sm={6} xs={12} key={product.id} className="mb-4" data-aos="zoom-in">
                  <ProductCard product={product} />
                </Col>
              ))}
            </Row>
          )}
        </Container>
      </section>
    </div>
  );
};

export default Catalog;
