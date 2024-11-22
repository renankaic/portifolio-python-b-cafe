const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

const modalDeleteCafe = document.getElementById("cafe-delete-confirm")
if (modalDeleteCafe) {
  modalDeleteCafe.addEventListener('show.bs.modal', event => {
    // Object that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const cafeId = button.getAttribute('data-bs-cafe-id')
    const cafeName = button.getAttribute('data-bs-cafe-name')
    // Update modal's content
    const modalCafeNameSpan = modalDeleteCafe.querySelector('.modal-body .cafe-name')
    modalCafeNameSpan.textContent = cafeName

    const modalBtnDelete = modalDeleteCafe.querySelector('.modal-footer button.btn-danger')
    modalBtnDelete.addEventListener('click', event => {
      fetch(`/cafe-delete/${cafeId}`, {
        method: 'DELETE'
      }).then(response => {
        if (!response.ok) {
          throw new Error(`Request error: ${response.statusText}`)
        }
        window.location.href = '/'
      }).catch(error => {
        console.error(error)
      })
    })
  })
}
