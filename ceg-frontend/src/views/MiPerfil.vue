<template>
  <div class="mi-perfil">
    <h2>Mi Perfil</h2>
    <p v-if="cargando">Cargando datos del perfil...</p>
    <div v-else-if="datosDisponibles">
      <div class="fila">
        <div class="columna">
          <h3>Nombre:</h3>
          <h2>{{ perfil.nombre }} {{ perfil.apellido }}</h2>
        </div>
        <div class="columna">
          <h3>Tipo de Socio:</h3>
          <h2>{{ perfil.tipoSocio }}</h2>
        </div>
      </div>
      
      <form @submit.prevent="actualizarPerfil">
        <div class="fila">
          <div class="columna">
            <h3>Email:</h3>
            <input type="email" id="email" v-model="perfil.email" required autocomplete="email">
          </div>
          <div class="columna">
            <h3>Teléfono:</h3>
            <input type="tel" id="telefono" v-model="perfil.telefono" autocomplete="tel">
          </div>
        </div>
        
        <div class="fila">
          <div class="columna">
            <h3>Contraseña Actual:</h3>
            <input type="password" id="passwordActual" v-model="passwordActual" autocomplete="current-password">
          </div>
          <div class="columna">
            <h3>Nueva Contraseña:</h3>
            <input type="password" id="passwordNueva" v-model="passwordNueva" autocomplete="new-password">
          </div>
        </div>
        
        <div class="fila">
          <div class="columna">
            <h3>Confirmar Nueva Contraseña:</h3>
            <input type="password" id="confirmPasswordNueva" v-model="confirmPasswordNueva" autocomplete="new-password">
          </div>
        </div>
        
        <button type="submit">Actualizar Perfil</button>
      </form>
    </div>
    <div v-else>
      <p>No se pudieron cargar los datos del perfil.</p>
      <button @click="cargarPerfil">Intentar cargar de nuevo</button>
    </div>
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
        nombre: '',
        apellido: '',
        tipoSocio: '',
        email: '',
        telefono: ''
      },
      passwordActual: '',
      passwordNueva: '',
      confirmPasswordNueva: '',
      mensaje: '',
      error: false,
      cargando: true,
      datosDisponibles: false
    }
  },
  mounted() {
    this.cargarPerfil();
  },
  methods: {
    async cargarPerfil() {
      this.cargando = true;
      this.datosDisponibles = false;
      try {
        // Primero, intentamos obtener los datos del login
        const datosLogin = JSON.parse(localStorage.getItem('userData')) || {};
        console.log('Datos del login:', datosLogin);

        // Luego, cargamos los datos específicos del socio
        const token = localStorage.getItem('token');
        console.log('Token:', token);
        const response = await axios.get('http://localhost:8000/socios/me', {
          headers: { Authorization: `Bearer ${token}` }
        });
        console.log('Datos del socio recibidos:', response.data);

        // Combinamos los datos del login y del socio
        this.perfil = {
          nombre: response.data.name || datosLogin.nombre || '',
          apellido: response.data.lastname || datosLogin.apellido || '',
          tipoSocio: response.data.type || datosLogin.tipoSocio || '',
          email: response.data.email || datosLogin.email || '',
          telefono: response.data.phone || datosLogin.telefono || ''
        };
        console.log('Perfil combinado:', this.perfil);
        this.datosDisponibles = true;
      } catch (error) {
        console.error('Error al cargar el perfil:', error);
        if (error.response) {
          console.error('Respuesta del servidor:', error.response.data);
        }
        this.mensaje = 'Error al cargar el perfil';
        this.error = true;
      } finally {
        this.cargando = false;
      }
    },
    async actualizarPerfil() {
      try {
        let token = localStorage.getItem('token');
        console.log('Token inicial:', token);
        if (this.isTokenExpired(token)) {
          console.log('Token expirado, intentando renovar...');
          token = await this.renewToken();
        }
        console.log('Token final enviado:', token);

        const updateData = {};
        if (this.perfil.telefono) updateData.phone = this.perfil.telefono;
        if (this.perfil.email) updateData.email = this.perfil.email;
        if (this.passwordNueva && this.passwordNueva === this.confirmPasswordNueva) {
          updateData.password = this.passwordNueva;
        }

        console.log('Datos a actualizar:', updateData);

        if (Object.keys(updateData).length === 0) {
          this.mensaje = 'No hay cambios para actualizar';
          this.error = false;
          return;
        }

        const headers = {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        };
        console.log('Headers de la solicitud:', headers);

        const response = await axios.put('http://localhost:8000/socios/me', updateData, { headers });
        
        console.log('Respuesta del servidor:', response.data);
        this.mensaje = 'Perfil actualizado con éxito';
        this.error = false;
        // Actualizar los datos locales con la respuesta del servidor
        this.perfil.telefono = response.data.phone || this.perfil.telefono;
        this.perfil.email = response.data.email || this.perfil.email;
        this.passwordActual = '';
        this.passwordNueva = '';
        this.confirmPasswordNueva = '';
      } catch (error) {
        console.error('Error al actualizar el perfil:', error);
        if (error.response) {
          console.log('Respuesta del servidor:', error.response.data);
          console.log('Estado de la respuesta:', error.response.status);
          console.log('Cabeceras de la respuesta:', error.response.headers);
        } else if (error.request) {
          console.log('No se recibió respuesta:', error.request);
        } else {
          console.log('Error:', error.message);
        }
        this.mensaje = error.response?.data?.detail || 'Error al actualizar el perfil';
        this.error = true;
      }
    },
    isTokenExpired(token) {
      if (!token) return true;
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));

      const { exp } = JSON.parse(jsonPayload);
      const now = Date.now() / 1000;
      const expired = now >= exp;
      console.log('Token expiration:', new Date(exp * 1000));
      console.log('Current time:', new Date(now * 1000));
      console.log('Token expired:', expired);
      return expired;
    },

    async renewToken() {
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        console.log('Refresh token:', refreshToken);
        if (!refreshToken) {
          throw new Error('No refresh token available');
        }
        const response = await axios.post('http://localhost:8000/token/refresh', {
          refresh_token: refreshToken
        });
        const newToken = response.data.access_token;
        localStorage.setItem('token', newToken);
        console.log('New token obtained:', newToken);
        return newToken;
      } catch (error) {
        console.error('Error al renovar el token:', error);
        // Redirigir al login si no se puede renovar el token
        this.$router.push('/login');
      }
    }
  }
}
</script>
<style scoped>
.mi-perfil {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.fila {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.columna {
  flex: 1;
  margin-right: 10px;
}

.columna:last-child {
  margin-right: 0;
}

h2 {
  margin-top: 5px;
  margin-bottom: 15px;
  font-size: 1.2em;
  font-weight: normal;
}

h3 {
  margin-bottom: 5px;
  font-weight: bold;
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
  margin-top: 15px;
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
