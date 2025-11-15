import Swal from 'sweetalert2'

// Configuração padrão para mobile
const defaultConfig = {
  customClass: {
    popup: 'mobile-alert',
    title: 'mobile-alert-title',
    content: 'mobile-alert-content',
    confirmButton: 'mobile-alert-btn mobile-alert-btn-confirm',
    cancelButton: 'mobile-alert-btn mobile-alert-btn-cancel'
  },
  buttonsStyling: false,
  allowOutsideClick: false,
  allowEscapeKey: false
}

export const showSuccess = (title, text = '') => {
  return Swal.fire({
    ...defaultConfig,
    icon: 'success',
    title,
    text,
    confirmButtonText: 'OK',
    timer: 3000,
    timerProgressBar: true
  })
}

export const showError = (title, text = '') => {
  return Swal.fire({
    ...defaultConfig,
    icon: 'error',
    title,
    text,
    confirmButtonText: 'OK'
  })
}

export const showConfirm = (title, text = '', confirmText = 'Sim', cancelText = 'Cancelar') => {
  return Swal.fire({
    ...defaultConfig,
    icon: 'warning',
    title,
    text,
    showCancelButton: true,
    confirmButtonText: confirmText,
    cancelButtonText: cancelText
  })
}

export const showInfo = (title, text = '') => {
  return Swal.fire({
    ...defaultConfig,
    icon: 'info',
    title,
    text,
    confirmButtonText: 'OK'
  })
}

// Função para tratar erros de API de forma genérica
export const handleApiError = (error, context = '') => {
  console.error(`[${context}] Erro detalhado:`, error)
  
  let userMessage = 'Erro inesperado. Tente novamente.'
  
  if (error.response) {
    const status = error.response.status
    const detail = error.response.data?.detail || ''
    
    console.error(`[${context}] Status: ${status}, Detail: ${detail}`)
    
    switch (status) {
      case 400:
        if (detail.includes('Login já existe')) {
          userMessage = 'Login já cadastrado. Escolha outro.'
        } else {
          userMessage = 'Dados inválidos. Verifique as informações.'
        }
        break
      case 401:
        if (detail.includes('Usuário não encontrado')) {
          userMessage = 'Usuário não cadastrado.'
        } else {
          userMessage = 'Login e senha incorretos.'
        }
        break
      case 404:
        userMessage = 'Serviço não encontrado. Tente mais tarde.'
        break
      case 500:
        userMessage = 'Erro interno do servidor. Tente mais tarde.'
        break
      default:
        userMessage = 'Erro de conexão. Verifique sua internet.'
    }
  } else if (error.request) {
    console.error(`[${context}] Erro de rede:`, error.request)
    userMessage = 'Sem conexão com o servidor. Verifique sua internet.'
  } else {
    console.error(`[${context}] Erro:`, error.message)
    userMessage = 'Erro inesperado. Tente novamente.'
  }
  
  return showError('Ops!', userMessage)
}