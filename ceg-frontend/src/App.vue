<template>
  <div id="app">
    <Navbar
      :isAuthenticated="isAuthenticated"
      :isAdmin="isAdmin"
      :isSocio="isSocio"
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
      isAuthenticated: false,
      isAdmin: false,
      isSocio: false
    }
  },
  created() {
    this.checkAuth()
  },
  methods: {
    async checkAuth() {
      const token = localStorage.getItem('token')
      console.log('Token encontrado:', token ? 'Presente' : 'No presente')
      
      if (!token) {
        this.resetAuthState()
        return
      }

      try {
        const response = await this.getUserInfo(token)
        this.updateAuthState(response.data)
      } catch (error) {
        console.error('Error al verificar el token:', error)
        this.handleAuthError()
      }
    },
    async getUserInfo(token) {
      try {
        const adminResponse = await axios.get('http://localhost:8000/admin/me', {
          headers: { Authorization: `Bearer ${token}` }
        })
        return { data: { ...adminResponse.data, role: 'admin' } }
      } catch (error) {
        if (error.response && error.response.status !== 401) {
          throw error
        }
      }

      try {
        const socioResponse = await axios.get('http://localhost:8000/socios/me', {
          headers: { Authorization: `Bearer ${token}` }
        })
        return { data: { ...socioResponse.data, role: 'socio' } }
      } catch (error) {
        throw error
      }
    },
    updateAuthState(userData) {
      this.isAuthenticated = true
      this.isAdmin = userData.role === 'admin'
      this.isSocio = userData.role === 'socio'
      console.log('Estado de autenticación actualizado:', { isAuthenticated: this.isAuthenticated, isAdmin: this.isAdmin, isSocio: this.isSocio })
      
      if (this.$route.path === '/login') {
        if (this.isAdmin) {
          this.$router.push('/administradores')
        } else if (this.isSocio) {
          this.$router.push('/socios')
        } else {
          this.$router.push('/')
        }
      }
    },
    resetAuthState() {
      this.isAuthenticated = false
      this.isAdmin = false
      this.isSocio = false
    },
    handleAuthError() {
      this.resetAuthState()
      localStorage.removeItem('token')
      if (this.$route.meta.requiresAuth) {
        this.$router.push('/login')
      }
    },
    logout() {
      this.resetAuthState()
      localStorage.removeItem('token')
      this.$router.push('/login')
    },
    handleLoginSuccess(userData) {
      console.log('Login exitoso, datos del usuario:', userData)
      this.updateAuthState(userData)
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