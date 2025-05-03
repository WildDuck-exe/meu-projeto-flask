// Carrossel de imagens e vídeos
let slideIndex = 1;
let videoSlideIndex = 1;

// Inicializar os carrosséis
showSlides(slideIndex);
showVideoSlides(videoSlideIndex);

// Funções para o carrossel de imagens (Fotos)
function moveCarousel(n) {
    showSlides(slideIndex += n);
}

function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.querySelectorAll('#acervo .carousel-item'); // Para as imagens
    let indicators = document.querySelectorAll('#acervo .carousel-indicators .indicator');

    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }

    for (i = 0; i < slides.length; i++) {
        slides[i].classList.remove("active");
    }
    for (i = 0; i < indicators.length; i++) {
        indicators[i].classList.remove("active");
    }

    slides[slideIndex - 1].classList.add("active");
    indicators[slideIndex - 1].classList.add("active");
}

// Funções para o carrossel de vídeos (Projetos)
function moveVideoCarousel(n) {
    showVideoSlides(videoSlideIndex += n);
}

function currentVideoSlide(n) {
    showVideoSlides(videoSlideIndex = n);
}

function showVideoSlides(n) {
    let i;
    let slides = document.querySelectorAll('#projetos .carousel-item'); // Para os vídeos
    let indicators = document.querySelectorAll('#projetos .carousel-indicators .indicator');

    if (n > slides.length) { videoSlideIndex = 1 }
    if (n < 1) { videoSlideIndex = slides.length }

    for (i = 0; i < slides.length; i++) {
        slides[i].classList.remove("active");
    }
    for (i = 0; i < indicators.length; i++) {
        indicators[i].classList.remove("active");
    }

    slides[videoSlideIndex - 1].classList.add("active");
    indicators[videoSlideIndex - 1].classList.add("active");
}

// Lógica para o modal "Saiba mais"
document.addEventListener('DOMContentLoaded', function() {
    const saibaMaisBtn = document.getElementById('saibaMaisBtn');
    const sobreModal = document.getElementById('sobreModal');
    const closeModalBtn = sobreModal.querySelector('.close-modal');

    // Abrir o modal ao clicar no botão "Saiba mais"
    saibaMaisBtn.addEventListener('click', function(e) {
        e.preventDefault();
        sobreModal.classList.add('show');
    });

    // Fechar o modal ao clicar no botão "X"
    closeModalBtn.addEventListener('click', function() {
        sobreModal.classList.remove('show');
    });

    // Fechar o modal ao clicar fora dele
    sobreModal.addEventListener('click', function(e) {
        if (e.target === sobreModal) {
            sobreModal.classList.remove('show');
        }
    });

    // Lógica para o formulário de inscrição
    const formModal = document.getElementById('formModal');
    const confirmacaoModal = document.getElementById('confirmacaoModal');
    const acessarFormularioBtn = document.getElementById('acessarFormulario');
    const closeFormModalBtn = formModal.querySelector('.close-modal');
    const formSteps = document.querySelectorAll('.form-step');
    const nextStepButtons = document.querySelectorAll('.next-step');
    const prevStepButtons = document.querySelectorAll('.prev-step');
    const currentStep = document.getElementById('current-step');
    const inscricaoForm = document.getElementById('inscricaoForm');
    const limparCamposBtn = document.getElementById('limpar-campos');
    const necessidadeEspecial = document.getElementById('necessidade_especial');
    const descricaoNecessidade = document.getElementById('descricao_necessidade');
    const cepInput = document.getElementById('cep');
    const ruaInput = document.getElementById('endereco_rua');
    const bairroInput = document.getElementById('endereco_bairro');
    const telefoneInput = document.getElementById('telefone');

    let currentStepIndex = 1;

    // Função para aplicar máscara de telefone
    function applyPhoneMask(input) {
        let value = input.value.replace(/\D/g, ''); // Remove tudo que não for dígito
        if (value.length > 11) value = value.substring(0, 11); // Limita a 11 dígitos
        if (value.length > 10) {
            // Formato para celular (11 dígitos): (XX) 9XXXX-XXXX
            value = value.replace(/^(\d{2})(\d{1})(\d{4})(\d{4})$/, '($1) $2$3-$4');
        } else if (value.length > 6) {
            // Formato para telefone fixo (10 dígitos): (XX) XXXX-XXXX
            value = value.replace(/^(\d{2})(\d{4})(\d{4})$/, '($1) $2-$3');
        } else if (value.length > 2) {
            // Formato parcial: (XX) XXXX
            value = value.replace(/^(\d{2})(\d{0,4})/, '($1) $2');
        } else if (value.length > 0) {
            // Apenas o DDD: (XX)
            value = value.replace(/^(\d{0,2})/, '($1');
        }
        input.value = value;
    }

    // Aplicar máscara enquanto o usuário digita
    telefoneInput.addEventListener('input', function() {
        applyPhoneMask(this);
        const errorMessage = document.getElementById('telefone_error');
        const digits = this.value.replace(/\D/g, '').length;
        if (digits < 10 && this.value) {
            errorMessage.style.display = 'block';
            errorMessage.textContent = 'Digite pelo menos 10 dígitos (ex: 71994091582).';
            this.style.borderColor = 'red';
        } else {
            errorMessage.style.display = 'none';
            this.style.borderColor = '';
        }
    });

    // Abrir o modal do formulário
    acessarFormularioBtn.addEventListener('click', function(e) {
        e.preventDefault();
        formModal.classList.add('show');
        showStep(1);
    });

    // Fechar o modal do formulário
    closeFormModalBtn.addEventListener('click', function() {
        formModal.classList.remove('show');
        resetForm();
    });

    // Fechar o modal do formulário ao clicar fora
    formModal.addEventListener('click', function(e) {
        if (e.target === formModal) {
            formModal.classList.remove('show');
            resetForm();
        }
    });

    // Navegação entre etapas
    nextStepButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (validateStep(currentStepIndex)) {
                if (currentStepIndex === 3) {
                    const necessidade = necessidadeEspecial.value;
                    if (necessidade === 'sim') {
                        descricaoNecessidade.style.display = 'block';
                    } else {
                        descricaoNecessidade.style.display = 'none';
                    }
                }
                showStep(currentStepIndex + 1);
            }
        });
    });

    prevStepButtons.forEach(button => {
        button.addEventListener('click', function() {
            showStep(currentStepIndex - 1);
        });
    });

    // Validação de etapa
    function validateStep(step) {
        const inputs = formSteps[step - 1].querySelectorAll('input[required], select[required], input[type="checkbox"][required]');
        let isValid = true;
        inputs.forEach(input => {
            if (input.type === 'checkbox') {
                if (!input.checked) {
                    isValid = false;
                    input.parentElement.style.color = 'red';
                } else {
                    input.parentElement.style.color = '';
                }
            } else if (input.id === 'telefone') {
                const digits = input.value.replace(/\D/g, '').length;
                if (digits < 10) {
                    isValid = false;
                    input.style.borderColor = 'red';
                    const errorMessage = document.getElementById('telefone_error');
                    if (errorMessage) {
                        errorMessage.style.display = 'block';
                        errorMessage.textContent = 'Digite pelo menos 10 dígitos (ex: 71994091582).';
                    }
                } else {
                    input.style.borderColor = '';
                    const errorMessage = document.getElementById('telefone_error');
                    if (errorMessage) errorMessage.style.display = 'none';
                }
            } else if (!input.value) {
                isValid = false;
                input.style.borderColor = 'red';
                const errorMessage = document.getElementById(`${input.id}_error`);
                if (errorMessage) {
                    errorMessage.style.display = 'block';
                    errorMessage.textContent = 'Este campo é obrigatório.';
                }
            } else {
                input.style.borderColor = '';
                const errorMessage = document.getElementById(`${input.id}_error`);
                if (errorMessage) errorMessage.style.display = 'none';
            }
        });
        return isValid;
    }

    // Exibir etapa
    function showStep(step) {
        formSteps.forEach(stepElement => {
            stepElement.classList.remove('active');
        });
        formSteps[step - 1].classList.add('active');
        currentStepIndex = step;
        currentStep.textContent = step;
        if (step === 5) {
            document.querySelectorAll('.prev-step')[2].style.display = 'none';
        } else {
            document.querySelectorAll('.prev-step').forEach(btn => btn.style.display = 'inline-block');
        }
    }

    // Validação em tempo real para e-mail
    const emailInput = document.getElementById('email');
    emailInput.addEventListener('input', function() {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const errorMessage = document.getElementById('email_error');
        if (!emailPattern.test(this.value) && this.value) {
            errorMessage.style.display = 'block';
            errorMessage.textContent = 'Por favor, insira um e-mail válido.';
            this.style.borderColor = 'red';
        } else {
            errorMessage.style.display = 'none';
            this.style.borderColor = '';
        }
    });

    // Busca de CEP (simulada para demonstração)
    cepInput.addEventListener('blur', function() {
        const cep = this.value.replace(/\D/g, '');
        if (cep.length === 8) {
            // Simulação de busca de CEP
            setTimeout(() => {
                ruaInput.value = 'Rua Exemplo';
                bairroInput.value = 'Bairro Exemplo';
            }, 1000);
        }
    });

    // Enviar formulário para o backend Flask
    inscricaoForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (validateStep(currentStepIndex)) {
            // Coletar os dados do formulário
            const formData = {
                nome_completo: document.getElementById('nome_completo').value,
                data_nascimento: document.getElementById('data_nascimento').value || null,
                genero: document.getElementById('genero').value || null,
                cpf: document.getElementById('cpf').value || null,
                rg: document.getElementById('rg').value || null,
                email: document.getElementById('email').value,
                telefone: document.getElementById('telefone').value,
                cep: document.getElementById('cep').value || null,
                endereco_rua: document.getElementById('endereco_rua').value || null,
                endereco_bairro: document.getElementById('endereco_bairro').value || null,
                endereco_numero: document.getElementById('endereco_numero').value || null,
                nome_evento_atividade: document.getElementById('nome_evento_atividade').value || null,
                area_interesse: document.getElementById('area_interesse').value || null,
                turno_preferencia: document.getElementById('turno_preferencia').value || null,
                necessidade_especial: document.getElementById('necessidade_especial').value === 'sim',
                descricao_necessidade: document.getElementById('descricao_necessidade_text').value || null,
                como_soube: document.getElementById('como_soube').value || null,
                concorda_termos: document.getElementById('concorda_termos').checked,
                autoriza_imagem: document.getElementById('autoriza_imagem').checked,
                assina_newsletter: document.getElementById('assina_newsletter').checked
            };

            // Enviar os dados para o backend Flask
            fetch('http://localhost:5000/api/inscricoes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Resposta do servidor:', data);
                if (data.message && data.message.includes('sucesso')) {
                    formModal.classList.remove('show');
                    confirmacaoModal.classList.add('show');
                    resetForm();
                } else {
                    alert('Erro ao enviar inscrição: ' + (data.error || 'Tente novamente.'));
                }
            })
            .catch(error => {
                console.error('Erro ao enviar inscrição:', error);
                alert('Ocorreu um erro ao enviar a inscrição. Verifique o console.');
            });
        }
    });

    // Fechar o modal de confirmação
    window.closeConfirmacaoModal = function() {
        confirmacaoModal.classList.remove('show');
    };

    confirmacaoModal.addEventListener('click', function(e) {
        if (e.target === confirmacaoModal) {
            confirmacaoModal.classList.remove('show');
        }
    });

    // Limpar campos
    limparCamposBtn.addEventListener('click', function() {
        resetForm();
    });

    function resetForm() {
        inscricaoForm.reset();
        showStep(1);
        descricaoNecessidade.style.display = 'none';
        document.querySelectorAll('input, select').forEach(input => {
            input.style.borderColor = '';
            const errorMessage = document.getElementById(`${input.id}_error`);
            if (errorMessage) errorMessage.style.display = 'none';
        });
        document.querySelectorAll('.form-group label').forEach(label => {
            label.style.color = '';
        });
    }

    // Atualizar visibilidade da descrição de necessidade especial
    necessidadeEspecial.addEventListener('change', function() {
        if (this.value === 'sim') {
            descricaoNecessidade.style.display = 'block';
        } else {
            descricaoNecessidade.style.display = 'none';
        }
    });
});