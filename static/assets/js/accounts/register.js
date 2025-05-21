document.addEventListener("DOMContentLoaded",()=>{
    document.getElementById('form-register').addEventListener('submit', (e)=>{
        this.preventDefault()
        
        const form = e.target;
        form = new FormData(form);

        // Envoit des données avec fetch
        fetch('/accounts/regidter/',{
            method:'POST',
            body:FormData,


        }).then(response => response.json())
        .then(data=>{

            // réinitialiser les erreurs précédentes
            document.querySelectorAll('.has-error').forEach(el =>{
                el.classList.remove('.has-error','has-feedback')
            })
            const small = el.querySelector('small.error-message')
            if(small){
                small.remove()
            }
            if (data.message){
                alert(data.message); // En cas de succès
            }
            else{
                // gérer les erreurs
                Object.keys(data).forEach(key => {
                    const field = document.querySelector(`[name="${key}"]`);

                    if (field){
                        // ajouter les classes d'erreurs
                        field.parentElement.classList('has-error','has-feedback')

                        // créer et afficher le message d'erreur

                        const errorMsg = document.createElement('small')
                        errorMsg.className = 'error-message form-text text-danger';

                        errorMsg.textContent = data[key];

                        field.parentNode.appendChild(errorMsg)
                    }
                })
            }
        }).catch(error => console.error('Erreur',error))

    })
})