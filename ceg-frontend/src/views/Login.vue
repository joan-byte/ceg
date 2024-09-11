<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <label for="role">Selecciona tu rol:</label>
        <select v-model="role" id="role" autocomplete="off" @change="updateInputType">
          <option value="socio">Socio</option>
          <option value="admin">Administrador</option>
        </select>
      </div>
      <div>
        <label :for="inputId">{{ inputLabel }}:</label>
        <input v-model="username" :type="inputType" :id="inputId" required :autocomplete="autocompleteType" />
      </div>
      <div>
        <label for="password">Password:</label>
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
      isLoading: false,
      inputType: 'email',
      inputId: 'email',
      inputLabel: 'Email',
      autocompleteType: 'email'
    }
  },
  methods: {
    updateInputType() {
      if (this.role === 'admin') {
        this.inputType = 'text';
        this.inputId = 'username';
        this.inputLabel = 'Nombre';
        this.autocompleteType = 'username';
      } else {
        this.inputType = 'email';
        this.inputId = 'email';
        this.inputLabel = 'Email';
        this.autocompleteType = 'email';
      }
    },
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
        
        // Guarda el token y el rol en el almacenamiento local
        localStorage.setItem('token', token);
        localStorage.setItem('userRole', this.role);

        console.log('Token guardado:', token); // Para depuración

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
          } else if (error.response.status === 422) {
            this.errorMessage = 'Datos de inicio de sesión incorrectos. Verifica tu ' + (this.role === 'admin' ? 'nombre de usuario' : 'email') + ' y contraseña.';
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
  },
  created() {
    this.updateInputType();
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
