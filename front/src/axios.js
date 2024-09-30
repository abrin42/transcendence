import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8080/api/test-api/', // Remplace par l'URL de ton API
  timeout: 1000,
  headers: {'Content-Type': 'application/json'}
});

export default instance;
