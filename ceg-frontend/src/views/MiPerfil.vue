<template>
    <div class="mi-perfil">
      <h2>Mi Perfil</h2>
      <form @submit.prevent="actualizarPerfil">
        <div>
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="perfil.email" required>
        </div>
        <div>
          <label for="telefono">Teléfono:</label>
          <input type="tel" id="telefono" v-model="perfil.telefono">
        </div>
        <div>
          <label for="password">Nueva Contraseña:</label>
          <input type="password" id="password" v-model="perfil.password">
        </div>
        <div>
          <label for="confirmPassword">Confirmar Nueva Contraseña:</label>
          <input type="password" id="confirmPassword" v-model="confirmPassword">
        </div>
        <button type="submit">Actualizar Perfil</button>
      </form>
      <p v-if="mensaje" :class="{ 'exito': !error, 'error': error }">{{ mensaje }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'MiPerfil',
    data() {
      return {
        perfil: {
          email: '',
          telefono: '',
          password: ''
        },
        confirmPassword: '',
        mensaje: '',
        error: false
      }
    },
    mounted() {
      this.cargarPerfil();
    },
    methods: {
      async cargarPerfil() {
        try {
          const response = await axios.get('http://localhost:8000/socios/me', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
          this.perfil.email = response.data.email;
          this.perfil.telefono = response.data.telefono;
        } catch (error) {
          console.error('Error al cargar el perfil:', error);
          this.mensaje = 'Error al cargar el perfil';
          this.error = true;
        }
      },
      async actualizarPerfil() {
        if (this.perfil.password && this.perfil.password !== this.confirmPassword) {
          this.mensaje = 'Las contraseñas no coinciden';
          this.error = true;
          return;
        }
  
        try {
          const datosActualizados = {
            email: this.perfil.email,
            telefono: this.perfil.telefono
          };
          if (this.perfil.password) {
            datosActualizados.password = this.perfil.password;
          }
  
          await axios.put('http://localhost:8000/socios/me', datosActualizados, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
  
          this.mensaje = 'Perfil actualizado con éxito';
          this.error = false;
          this.perfil.password = '';
          this.confirmPassword = '';
        } catch (error) {
          console.error('Error al actualizar el perfil:', error);
          this.mensaje = 'Error al actualizar el perfil';
          this.error = true;
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .mi-perfil {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
  }
  
  form div {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  
  .exito {
    color: green;
  }
  
  .error {
    color: red;
  }
  </style>