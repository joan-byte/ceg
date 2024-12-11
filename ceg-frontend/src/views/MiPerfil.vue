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

        <div class="cambiar-password">
          <button 
            type="button" 
            class="toggle-password-section" 
            @click="mostrarSeccionPassword = !mostrarSeccionPassword">
            {{ mostrarSeccionPassword ? 'Cancelar cambio de contraseña' : 'Cambiar contraseña' }}
          </button>
        </div>
        
        <div v-if="mostrarSeccionPassword" class="password-section">
          <div class="fila">
            <div class="columna">
              <h3>Nueva Contraseña:</h3>
              <div class="password-field">
                <input 
                  type="password"
                  id="passwordNueva" 
                  v-model="passwordNueva" 
                  autocomplete="new-password">
                <button 
                  type="button" 
                  class="toggle-password" 
                  @click="togglePasswordVisibility('nueva')">
                  {{ mostrarPasswordNueva ? '🙈' : '👁️' }}
                </button>
              </div>
            </div>
            <div class="columna">
              <h3>Confirmar Nueva Contraseña:</h3>
              <div class="password-field">
                <input 
                  type="password"
                  id="confirmPasswordNueva" 
                  v-model="confirmPasswordNueva" 
                  autocomplete="new-password">
                <button 
                  type="button" 
                  class="toggle-password" 
                  @click="togglePasswordVisibility('confirm')">
                  {{ mostrarConfirmPassword ? '🙈' : '👁️' }}
                </button>
              </div>
            </div>
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
      passwordNueva: '',
      confirmPasswordNueva: '',
      mensaje: '',
      error: false,
      cargando: true,
      datosDisponibles: false,
      mostrarPasswordNueva: false,
      mostrarConfirmPassword: false,
      mostrarSeccionPassword: false
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
        if (!token) {
          throw new Error('No hay token de autenticación');
        }
        console.log('Token:', token);
        const response = await axios.get('http://192.168.10.21:8000/socios/me', {
          headers: { Authorization: `Bearer ${token}` }
        });
        console.log('Datos del socio recibidos:', response.data);

        if (!response.data) {
          throw new Error('No se recibieron datos del servidor');
        }

        // Combinamos los datos del login y del socio
        this.perfil = {
          nombre: response.data.name || '',
          apellido: response.data.lastname || '',
          tipoSocio: response.data.type || '',
          email: response.data.email || '',
          telefono: response.data.phone || ''
        };

        console.log('Perfil combinado:', this.perfil);
        this.datosDisponibles = true;
        this.mensaje = '';
        this.error = false;
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

        // Validar contraseñas si se están actualizando
        if (this.passwordNueva || this.confirmPasswordNueva) {
          if (this.passwordNueva !== this.confirmPasswordNueva) {
            this.mensaje = 'Las contraseñas no coinciden';
            this.error = true;
            return;
          }
        }

        const updateData = {};
        if (this.perfil.telefono) updateData.phone = this.perfil.telefono;
        if (this.perfil.email) updateData.email = this.perfil.email;
        if (this.passwordNueva) updateData.password = this.passwordNueva;

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

        const response = await axios.put('http://192.168.10.21:8000/socios/me', updateData, { headers });
        
        console.log('Respuesta del servidor:', response.data);
        this.mensaje = 'Perfil actualizado con éxito';
        this.error = false;
        // Actualizar los datos locales con la respuesta del servidor
        this.perfil.telefono = response.data.phone || this.perfil.telefono;
        this.perfil.email = response.data.email || this.perfil.email;
        this.passwordNueva = '';
        this.confirmPasswordNueva = '';
        this.mostrarPasswordNueva = false;
        this.mostrarConfirmPassword = false;
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
          throw new Error('No hay refresh token disponible');
        }
        
        const response = await axios.post('http://192.168.10.21:8000/auth/refresh', {
          refresh_token: refreshToken
        });

        if (response.data && response.data.access_token) {
          localStorage.setItem('token', response.data.access_token);
          return response.data.access_token;
        } else {
          throw new Error('No se pudo renovar el token');
        }
      } catch (error) {
        console.error('Error al renovar el token:', error);
        // Forzar logout si no se puede renovar el token
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('userData');
        this.$router.push('/login');
        throw new Error('Sesión expirada, por favor inicie sesión nuevamente');
      }
    },

    togglePasswordVisibility(field) {
      let input;
      switch(field) {
        case 'nueva':
          input = document.getElementById('passwordNueva');
          this.mostrarPasswordNueva = !this.mostrarPasswordNueva;
          if (input) input.type = this.mostrarPasswordNueva ? 'text' : 'password';
          break;
        case 'confirm':
          input = document.getElementById('confirmPasswordNueva');
          this.mostrarConfirmPassword = !this.mostrarConfirmPassword;
          if (input) input.type = this.mostrarConfirmPassword ? 'text' : 'password';
          break;
      }

      // Forzar reflow para iOS
      if (input) {
        const cursorPos = input.selectionStart;
        requestAnimationFrame(() => {
          input.blur();
          input.focus();
          input.setSelectionRange(cursorPos, cursorPos);
        });
      }
    },
    maskPassword(password) {
      return '•'.repeat(password.length);
    },
    updatePassword(event, field) {
      const value = event.target.value;
      if (field === 'nueva') {
        // Si el valor es más corto que la contraseña actual y son todos puntos,
        // significa que el usuario está borrando caracteres
        if (value.length < this.passwordNueva.length && value.match(/^[•]+$/)) {
          this.passwordNueva = this.passwordNueva.slice(0, -1);
        } 
        // Si el valor es más largo que la contraseña actual y termina en un carácter que no es punto,
        // significa que el usuario está añadiendo caracteres
        else if (value.length > this.passwordNueva.length && !value.endsWith('•')) {
          this.passwordNueva += value[value.length - 1];
        }
      } else if (field === 'confirm') {
        if (value.length < this.confirmPasswordNueva.length && value.match(/^[•]+$/)) {
          this.confirmPasswordNueva = this.confirmPasswordNueva.slice(0, -1);
        } else if (value.length > this.confirmPasswordNueva.length && !value.endsWith('•')) {
          this.confirmPasswordNueva += value[value.length - 1];
        }
      }
    },
    showPassword(field) {
      const input = document.getElementById(field === 'nueva' ? 'passwordNueva' : 'confirmPasswordNueva');
      if (input) {
        input.type = 'text';
        if (field === 'nueva') {
          this.mostrarPasswordNueva = true;
        } else {
          this.mostrarConfirmPassword = true;
        }
      }
    },
    hidePassword(field) {
      const input = document.getElementById(field === 'nueva' ? 'passwordNueva' : 'confirmPasswordNueva');
      if (input) {
        input.type = 'password';
        if (field === 'nueva') {
          this.mostrarPasswordNueva = false;
        } else {
          this.mostrarConfirmPassword = false;
        }
      }
    },
    handlePasswordInput(event, field) {
      const value = event.target.value;
      if (field === 'nueva') {
        this.passwordNueva = value;
      } else {
        this.confirmPasswordNueva = value;
      }
    },
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

.password-field {
  position: relative;
  width: 100%;
}

.password-field input {
  width: 100%;
  height: 35px;
  padding: 8px 35px 8px 8px;
  box-sizing: border-box;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.toggle-password {
  position: absolute;
  top: 1px;
  right: 1px;
  height: calc(100% - 2px);
  width: 35px;
  background: none;
  border: none;
  border-left: 1px solid #ddd;
  cursor: pointer;
  padding: 0;
  margin: 0;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0 4px 4px 0;
}

.toggle-password:hover {
  background: #f5f5f5;
}

input::placeholder {
  color: #999;
}

.password-hidden {
  -webkit-text-security: disc;
}

.password-field input {
  width: 100%;
  height: 35px;
  padding: 8px 35px 8px 8px;
  box-sizing: border-box;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px; /* Tamaño mínimo recomendado para iOS */
  -webkit-appearance: none; /* Prevenir estilo nativo de iOS */
  appearance: none;
}

.cambiar-password {
  margin: 20px 0;
  text-align: left;
}

.toggle-password-section {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.toggle-password-section:hover {
  background-color: #45a049;
}

.password-section {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f9f9f9;
}
</style>
