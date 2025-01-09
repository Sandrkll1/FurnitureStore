// src/pages/Profile.js
import React, { useState, useEffect, useContext } from 'react';
import { Container, Form, Button, Alert, Spinner } from 'react-bootstrap';
import axios from '../api/axiosConfig';
import { AuthContext } from '../context/AuthContext';

const Profile = () => {
  const { fetchUserProfile } = useContext(AuthContext);
  const [profile, setProfile] = useState({
    name: '',
    email: '',
    birthday: '', // Дата рождения
    image_url: '',
  });
  const [originalProfile, setOriginalProfile] = useState(null); // Исходные данные профиля
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  // Загрузка профиля при первом рендере
  useEffect(() => {
    const loadProfile = async () => {
      try {
        const response = await axios.get('/user/profile');
        const userProfile = response.data;

        // Преобразуем дату рождения в формат YYYY-MM-DD
        const formattedBirthday = userProfile.birthday
          ? userProfile.birthday.split('T')[0]
          : '';

        setProfile({
          ...userProfile,
          birthday: formattedBirthday,
        });
        setOriginalProfile({
          ...userProfile,
          birthday: formattedBirthday,
        });
      } catch (err) {
        console.error('Ошибка при загрузке профиля:', err);
      }
    };
    loadProfile();
  }, []);

  const handleEditToggle = () => {
    setIsEditing(true);
    setMessage(null);
    setError(null);
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setProfile(originalProfile); // Возвращаем исходные данные профиля
  };

  const handleSave = async (e) => {
    e.preventDefault();

    // Проверяем, есть ли изменения
    if (
      profile.name === originalProfile.name &&
      profile.birthday === originalProfile.birthday
    ) {
      setMessage('Нет изменений для сохранения.');
      setIsEditing(false);
      return;
    }

    setIsLoading(true);
    setMessage(null);
    setError(null);

    try {
      const response = await axios.put('/user/profile', {
        name: profile.name,
        birthday: profile.birthday || null, // Отправляем null, если дата не указана
      });
      const updatedProfile = response.data;

      // Обновляем профиль и сохраняем исходные данные
      setProfile({
        ...updatedProfile,
        birthday: updatedProfile.birthday
          ? updatedProfile.birthday.split('T')[0]
          : '',
      });
      setOriginalProfile({
        ...updatedProfile,
        birthday: updatedProfile.birthday
          ? updatedProfile.birthday.split('T')[0]
          : '',
      });

      setMessage('Профиль успешно обновлен.');
      setIsEditing(false);

      if (fetchUserProfile) {
        fetchUserProfile(); // Обновляем контекст пользователя
      }
    } catch (err) {
      console.error('Ошибка при обновлении профиля:', err);
      setError('Не удалось обновить профиль. Попробуйте снова.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container className="my-5" style={{ maxWidth: '600px' }}>
      <h2 className="text-center mb-4">Профиль пользователя</h2>
      {message && <Alert variant="success">{message}</Alert>}
      {error && <Alert variant="danger">{error}</Alert>}

      {isLoading ? (
        <div className="text-center">
          <Spinner animation="border" />
        </div>
      ) : (
        <Form onSubmit={handleSave}>
          <Form.Group className="mb-3">
            <Form.Label>Имя</Form.Label>
            <Form.Control
              type="text"
              value={profile.name}
              disabled={!isEditing}
              onChange={(e) => setProfile({ ...profile, name: e.target.value })}
              required
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Email</Form.Label>
            <Form.Control type="email" value={profile.email} disabled />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Дата рождения</Form.Label>
            <Form.Control
              type="date"
              value={profile.birthday || ''}
              disabled={!isEditing}
              onChange={(e) =>
                setProfile({ ...profile, birthday: e.target.value })
              }
            />
          </Form.Group>
          {profile.image_url && (
            <div className="mb-3 text-center">
              <img
                src={profile.image_url}
                alt="Аватар"
                style={{ maxWidth: '150px', borderRadius: '50%' }}
              />
            </div>
          )}
          {isEditing ? (
            <div className="d-flex justify-content-between">
              <Button variant="secondary" onClick={handleCancelEdit}>
                Отмена
              </Button>
              <Button variant="primary" type="submit">
                Сохранить
              </Button>
            </div>
          ) : (
            <Button
              variant="secondary"
              onClick={handleEditToggle}
              className="w-100"
            >
              Редактировать
            </Button>
          )}
        </Form>
      )}
    </Container>
  );
};

export default Profile;
