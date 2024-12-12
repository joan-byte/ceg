// Configuración de la URL base del backend
export const getBaseURL = () => {
    return window.location.hostname === 'localhost' ? 'http://localhost:8000' : 'http://192.168.10.21:8000';
};

export default {
    getBaseURL
}; 