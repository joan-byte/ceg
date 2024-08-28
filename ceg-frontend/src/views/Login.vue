<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <label for="role">Selecciona tu rol:</label>
        <select v-model="role" id="role" autocomplete="off">
          <option value="socio">Socio</option>
          <option value="admin">Administrador</option>
        </select>
      </div>
      <div>
        <label for="username">Email/Nombre:</label>
        <!-- Añadir el atributo autocomplete adecuado -->
        <input v-model="username" type="text" id="username" required autocomplete="username" />
      </div>
      <div>
        <label for="password">Password:</label>
        <!-- Añadir el atributo autocomplete adecuado -->
        <input v-model="password" type="password" id="password" required autocomplete="current-password" />
      </div>
      <button type="submit" :disabled="isLoading">{{ isLoading ? 'Cargando...' : 'Login' }}</button>
    </form>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      username: '',
      password: '',
      role: 'socio',
      errorMessage: '',
      isLoading: false
    }
  },
  methods: {
    async login() {
      this.isLoading = true;
      this.errorMessage = '';
      try {
        const tokenUrl = this.role === 'admin' 
          ? 'http://localhost:8000/token_admin' 
          : 'http://localhost:8000/token_socio';

        const formData = new URLSearchParams();
        formData.append('username', this.username);
        formData.append('password', this.password);

        const tokenResponse = await axios.post(tokenUrl, formData);
        const token = tokenResponse.data.access_token;
        localStorage.setItem('token', token);

        // Guardar el rol del usuario en localStorage
        localStorage.setItem('userRole', this.role);

        const userUrl = this.role === 'admin'
          ? 'http://localhost:8000/admin/me'
          : 'http://localhost:8000/socios/me';

        const userResponse = await axios.get(userUrl, {
          headers: { Authorization: `Bearer ${token}` }
        });

        this.$emit('login-success', {
          user: userResponse.data,
          role: this.role
        });

        this.$router.push('/');
      } catch (error) {
        if (error.response) {
          if (error.response.status === 401) {
            this.errorMessage = 'Credenciales incorrectas. Por favor, inténtalo de nuevo.';
          } else {
            this.errorMessage = 'Error en el servidor. Por favor, inténtalo más tarde.';
          }
        } else if (error.request) {
          this.errorMessage = 'No se pudo conectar con el servidor. Verifica tu conexión.';
        } else {
          this.errorMessage = 'Error al procesar la solicitud. Por favor, inténtalo de nuevo.';
        }
        console.error('Error durante el login:', error);
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input,
select {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>