<template>
  <div id="app">
    <Navbar
      :isAuthenticated="authState.isAuthenticated"
      :isAdmin="authState.isAdmin"
      :isSocio="authState.isSocio"
      @logout="logout"
    />
    <router-view @login-success="handleLoginSuccess" />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    Navbar
  },
  data() {
    return {
      authState: {
        isAuthenticated: false,
        isAdmin: false,
        isSocio: false
      }
    }
  },
  created() {
    this.checkAuth()
  },
  methods: {
    async checkAuth() {
      const token = localStorage.getItem('token');
      const userRole = localStorage.getItem('userRole');
      
      if (token && userRole) {
        try {
          let userInfo;
          if (userRole === 'admin') {
            userInfo = await this.getUserInfo('http://localhost:8000/admin/me');
          } else if (userRole === 'socio') {
            userInfo = await this.getUserInfo('http://localhost:8000/socios/me');
          }
          
          if (userInfo) {
            this.updateAuthState(true, userRole === 'admin', userRole === 'socio');
          } else {
            this.logout();
          }
        } catch (error) {
          console.error('Error al verificar la autenticación:', error);
          this.logout();
        }
      } else {
        this.logout();
      }
    },

    async getUserInfo(url) {
      const token = localStorage.getItem('token');
      try {
        const response = await axios.get(url, {
          headers: { Authorization: `Bearer ${token}` }
        });
        return response.data;
      } catch (error) {
        console.error('Error al obtener información del usuario:', error);
        return null;
      }
    },

    updateAuthState(isAuthenticated, isAdmin, isSocio) {
      this.authState.isAuthenticated = isAuthenticated;
      this.authState.isAdmin = isAdmin;
      this.authState.isSocio = isSocio;
    },

    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('userRole');
      this.updateAuthState(false, false, false);
      this.$router.push('/login');
    },

    handleLoginSuccess(userData) {
      console.log('Login exitoso, datos del usuario:', userData)
      this.updateAuthState(true, userData.role === 'admin', userData.role === 'socio')
    }
  }
}
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>