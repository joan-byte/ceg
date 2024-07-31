<template>
  <div>
    <h1 class="title centered">Agregar Pista</h1>
    <div class="card">
      <div class="form-group">
        <label for="nombre" class="bold">Nombre</label>
        <input id="nombre" name="nombre" v-model="newPista.name" type="text" class="input-field" autocomplete="off" />
      </div>
      <div class="form-group">
        <label for="tipo_pista" class="bold">Tipo de Pista</label>
        <select id="tipo_pista" name="tipo_pista" v-model="newPista.tipo_pista" class="input-field" autocomplete="off">
          <option value="Tenis">Tenis</option>
          <option value="Padel">Padel</option>
          <option value="Pickleball">Pickleball</option>
        </select>
      </div>
      <div class="form-group">
        <label for="tiempo_juego" class="bold">Tiempo de Juego</label>
        <input id="tiempo_juego" name="tiempo_juego" v-model="newPista.tiempo_juego" type="number" class="input-field" autocomplete="off" />
      </div>
      <div class="form-group">
        <label for="individuales" class="bold">Individuales</label>
        <select id="individuales" name="individuales" v-model="newPista.individuales" class="input-field" autocomplete="off">
          <option :value="true">Sí</option>
          <option :value="false">No</option>
        </select>
      </div>
      <div class="btn-container">
        <button @click="createPista" class="btn btn-primary">Crear</button>
        <button @click="resetForm" class="btn btn-secondary">Cancelar</button>
      </div>
    </div>
    <h1 class="title right-title">Pistas Existentes</h1>
    <div class="cards-container">
      <div v-for="pista in pistas" :key="pista.id" class="card-existing">
        <div v-if="isEditing && editingPista.id === pista.id">
          <div class="form-group">
            <label for="edit-nombre" class="bold">Nombre</label>
            <input id="edit-nombre" v-model="editingPista.name" type="text" class="input-field" />
          </div>
          <div class="form-group">
            <label for="edit-tipo_pista" class="bold">Tipo de Pista</label>
            <select id="edit-tipo_pista" v-model="editingPista.tipo_pista" class="input-field">
              <option value="Tenis">Tenis</option>
              <option value="Padel">Padel</option>
              <option value="Pickleball">Pickleball</option>
            </select>
          </div>
          <div class="form-group">
            <label for="edit-tiempo_juego" class="bold">Tiempo de Juego</label>
            <input id="edit-tiempo_juego" v-model="editingPista.tiempo_juego" type="number" class="input-field" />
          </div>
          <div class="form-group">
            <label for="edit-individuales" class="bold">Individuales</label>
            <select id="edit-individuales" v-model="editingPista.individuales" class="input-field">
              <option :value="true">Sí</option>
              <option :value="false">No</option>
            </select>
          </div>
          <div class="btn-container">
            <button @click="updatePista(pista.id)" class="btn btn-primary">Guardar</button>
            <button @click="cancelEdit" class="btn btn-secondary">Cancelar</button>
          </div>
        </div>
        <div v-else>
          <div class="form-group">
            <label for="nombre" class="bold">Nombre</label>
            <div id="nombre">{{ pista.name }}</div>
          </div>
          <div class="form-group">
            <label for="tipo_pista" class="bold">Tipo de Pista</label>
            <div id="tipo_pista">{{ pista.tipo_pista }}</div>
          </div>
          <div class="form-group">
            <label for="tiempo_juego" class="bold">Tiempo de Juego</label>
            <div id="tiempo_juego">{{ pista.tiempo_juego }}</div>
          </div>
          <div class="form-group">
            <label for="individuales" class="bold">Individuales</label>
            <div id="individuales">{{ pista.individuales ? 'Sí' : 'No' }}</div>
          </div>
          <div class="btn-container">
            <button @click="editPista(pista)" class="btn btn-primary">Modificar</button>
            <button @click="deletePista(pista.id)" class="btn btn-danger">Eliminar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      newPista: {
        name: '',
        tipo_pista: 'Tenis',
        tiempo_juego: 0,
        individuales: false
      },
      pistas: [],
      isEditing: false,
      editingPista: null
    };
  },
  methods: {
    fetchPistas() {
      axios.get('http://localhost:8000/pistas/')
        .then(response => {
          this.pistas = response.data;
        })
        .catch(error => {
          console.error('Hubo un error al obtener las pistas:', error);
        });
    },
    createPista() {
      axios.post('http://localhost:8000/pistas/', this.newPista)
        .then(response => {
          this.pistas.push(response.data);
          this.resetForm();
        })
        .catch(error => {
          console.error('Hubo un error al crear la pista:', error);
        });
    },
    editPista(pista) {
      this.isEditing = true;
      this.editingPista = { ...pista };
    },
    updatePista(pistaId) {
      axios.put(`http://localhost:8000/pistas/${pistaId}`, this.editingPista)
        .then(response => {
          const index = this.pistas.findIndex(p => p.id === pistaId);
          if (index !== -1) {
            this.pistas.splice(index, 1, response.data);
          }
          this.isEditing = false;
          this.editingPista = null;
        })
        .catch(error => {
          console.error('Hubo un error al actualizar la pista:', error);
        });
    },
    deletePista(pistaId) {
      axios.delete(`http://localhost:8000/pistas/${pistaId}`)
        .then(() => {
          this.pistas = this.pistas.filter(pista => pista.id !== pistaId);
        })
        .catch(error => {
          console.error('Hubo un error al eliminar la pista:', error);
        });
    },
    resetForm() {
      this.newPista = {
        name: '',
        tipo_pista: 'Tenis',
        tiempo_juego: 0,
        individuales: false
      };
    },
    cancelEdit() {
      this.isEditing = false;
      this.editingPista = null;
    }
  },
  mounted() {
    this.fetchPistas();
  }
};
</script>

<style>
.title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.centered {
  text-align: center;
}

.right-title {
  margin-left: 20px;
}

.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  width: 20%;
  margin: 0 auto;
}

.card-existing {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin: 10px;
  width: 20%;
  display: inline-block;
  vertical-align: top;
}

.form-group {
  margin-bottom: 15px;
}

.input-field {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.bold {
  font-weight: bold;
}

.btn-container {
  display: flex;
  justify-content: space-between;
}

.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.cards-container {
  display: flex;
  flex-wrap: wrap;
}
</style>