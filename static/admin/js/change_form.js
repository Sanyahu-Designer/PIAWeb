'use strict';
{
    const inputTags = ['BUTTON', 'INPUT', 'SELECT', 'TEXTAREA'];
    const constantsElement = document.getElementById('django-admin-form-add-constants');
    
    // Verificar se o elemento existe antes de tentar acessar suas propriedades
    if (constantsElement && constantsElement.dataset && constantsElement.dataset.modelName) {
        const modelName = constantsElement.dataset.modelName;
        if (modelName) {
            const form = document.getElementById(modelName + '_form');
            if (form) {
                for (const element of form.elements) {
                    // HTMLElement.offsetParent returns null when the element is not
                    // rendered.
                    if (inputTags.includes(element.tagName) && !element.disabled && element.offsetParent) {
                        element.focus();
                        break;
                    }
                }
            }
        }
    }
}
