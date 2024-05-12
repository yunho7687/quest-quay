$(document).ready(function () {
  const submitPostBtn = $("#submit-post-btn");
  const submit = $("#submit-post");
  const navCreatePostBtn = $("#nav-create-post");

  submitPostBtn.click(function (e) {
    e.preventDefault();
    submit.click();
  });
  navCreatePostBtn.click(function (e) {
    e.preventDefault();
    $(".modal-backdrop.fade.show").addClass("blur-effect opacity-100");
  });
});
