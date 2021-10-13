let lorem = `Lorem ipsum dolor sit amet consectetur, adipisicing elit. Neque magni facilis beatae? 
Delectus cum pariatur consectetur incidunt libero a, tenetur odit possimus laboriosam. Quam, 
adipisci incidunt autem rerum quidem suscipit?
Lorem ipsum dolor sit amet consectetur adipisicing elit. Molestias quos magni voluptatem earum, 
dolorum autem nesciunt eligendi aperiam ab eveniet voluptas qui fugit cupiditate, minus facere 
nemo error! Eum, tempora.`;

let texts = [[lorem] , [`${lorem}<br><br>${lorem}`] , [lorem]];

(function () {
  let comment = document.querySelector('#feedbacks');
  if (texts.length != 0) {
    for (let i = 0; i < texts.length; i++) {
      comment.innerHTML += `
        <div class="row">
          <div class="col-2 pic-feedback">
            <img src="/static/img/profile.png" alt="Imágen User-profile">
          </div>
          <div class="col-8"> 
            <div class="row_1 info-feedback">
              <div>
                <h2>Empresa</h2>
                <div class="name_loc">
                  <i class="fas fa-user-alt"></i>
                  <p>&nbsp;Nombre gerente</p>
                </div>
              </div>
              <div>
                <p>30 Sep, 2021</p>
              </div>
            </div>
            <div class="row_2">
              <div class="feedback_text">
                <h5>
                  ${texts[i]}
                </h5>
              </div>
            </div>
          </div>
        </div>
      <br>
      `;
    }
  }else{
    comment.innerHTML = 'No hay retroalimentaciones'
  }
})();