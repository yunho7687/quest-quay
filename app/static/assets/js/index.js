$(document).ready(function () {
  const submitPost = $("#submit-post");
  const submit = $("#submit");
  const navCreatePostBtn = $("#nav-create-post");

  submitPost.click(function (e) {
    e.preventDefault();
    submit.click();
  });
  navCreatePostBtn.click(function(e){
    e.preventDefault()
     $(".modal-backdrop.fade.show").addClass("blur-effect opacity-100");
  })
});
