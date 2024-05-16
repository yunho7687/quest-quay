$(document).ready(function () {
  const submitPostBtn = $("#submit-post-btn");
  const submit = $("#submit-post");
  const navCreatePostBtn = $("#nav-create-post");
  const likeCommentForm = $("form.like-comment-form");
  const saveCommentForm = $("form.save-comment-form");
  const likePostForm = $("form.like-post-form");
  const savePostForm = $("form.save-post-form");
  const uploadFileElement = $('[name="uploadFile"]');
  const submitComment = $("#submit-comment");

  submitComment.on("click", function (e) {

    if ($("#comment").val() != "" ){
      $(this).prop("disabled", true);
      $(this).attr("value", "uploading...");
      const jqform = $(this).parent("form");
      const url = jqform.attr("action")
      const form = jqform.get(0);
      const formData = new FormData(form)
      
    $.ajax({
      type: "POST",
      url: url,
      data: formData, // 使用FormData对象
      processData: false, // 不要处理数据
      contentType: false, // 不要设置内容类型
      success: function (response, status) {
      window.scrollTo(0, 0)

       setTimeout(() => {
        location.reload();

       }, 50);
       
     
      },
      error: function (xhr, status, error) {
        console.error("Error liking comment: " + error); // Error logging
      },
    });

    }

  });
  uploadFileElement.addClass("form-control mt-2");
  $(".like-comment").each(function () {
    $(this).on("click", function () {
      $(this).children("form").submit();
    });
  });

  $(".save-comment").each(function () {
    $(this).on("click", function () {
      $(this).children("form").submit();
    });
  });

  submitPostBtn.click(function (e) {
    e.preventDefault();
    submit.click();
  });
  navCreatePostBtn.click(function (e) {
    e.preventDefault();
    $(".modal-backdrop.fade.show").addClass("blur-effect opacity-100");
  });

  likePostForm.submit(function (e) {
    e.preventDefault();

    $(e.target.parentNode).prop("disabled", true);
    $(e.target.parentNode).children("svg").addClass("visually-hidden");
    $(e.target.parentNode).children("span").addClass("spinner-border");

    const form = $(this);
    const url = form.attr("action"); // Get the action attribute from the form
    $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // Serialize form data for submission
      success: function (response, status) {
        $(e.target.parentNode).prop("disabled", false);
        // update the UI
        if (response.action == "like") {
          // when like
          let newLikes = response.likes;
          $(e.target.parentNode).addClass("text-primary");

          $(e.target.parentNode).children("svg").removeClass("visually-hidden");
          $(e.target.parentNode).children("span").removeClass("spinner-border");
          console.log(newLikes);
          $(e.target.parentNode)
            .closest("div.obj")
            .find(".text-bg-info")
            .first()
            .text(newLikes + " like");
        } else {
          // when dislike
          let newLikes = response.likes;
          $(e.target.parentNode).removeClass("text-primary");

          $(e.target.parentNode).children("svg").removeClass("visually-hidden");
          $(e.target.parentNode).children("span").removeClass("spinner-border");
          $(e.target.parentNode)
            .closest("div.obj")
            .find(".text-bg-info")
            .first()
            .text(newLikes + " like");
          console.log(newLikes);


        }
      },
      error: function (xhr, status, error) {
        console.error("Error liking comment: " + error); // Error logging
      },
    });
  });

  savePostForm.submit(function (e) {
    e.preventDefault();

    $(e.target.parentNode).prop("disabled", true);
    $(e.target.parentNode).children("svg").addClass("visually-hidden");
    $(e.target.parentNode).children("span").addClass("spinner-border");

    const form = $(this);
    const url = form.attr("action"); // Get the action attribute from the form

    $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // Serialize form data for submission
      success: function (response, status) {
        $(e.target.parentNode).prop("disabled", false);
        // update the UI
        if (response.action == "save") {
          let newSaves = response.saves;
          console.log(newSaves);
          $(e.target.parentNode)
            .closest("div.obj")
            .find(".text-bg-success")
            .first()
            .text(newSaves + " save");

          $(e.target.parentNode).addClass("text-warning");

          $(e.target.parentNode).children("svg").removeClass("visually-hidden");
          $(e.target.parentNode).children("span").removeClass("spinner-border");
        } else {
          let newSaves = response.saves;
          console.log(newSaves);

          $(e.target.parentNode)
            .closest("div.obj")
            .find(".text-bg-success")
            .first()
            .text(newSaves + " save");

          $(e.target.parentNode).removeClass("text-warning");

          $(e.target.parentNode).children("svg").removeClass("visually-hidden");
          $(e.target.parentNode).children("span").removeClass("spinner-border");
        }
      },
      error: function (xhr, status, error) {
        console.error("Error liking comment: " + error); // Error logging
      },
    });
  });

  saveCommentForm.submit(function (e) {
    e.preventDefault();
    $(e.target.parentNode).prop("disabled", true);
    $(e.target.parentNode).children("svg").addClass("visually-hidden");
    $(e.target.parentNode).children("span").addClass("spinner-border");

    const form = $(this);
    const url = form.attr("action"); // Get the action attribute from the form
    $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // Serialize form data for submission
      success: function (response, status) {
        $(e.target.parentNode).prop("disabled", false);
        // update the UI
        if (response.action == "save") {
          $(e.target.parentNode).addClass("text-warning");

          $(e.target.parentNode).children("svg").removeClass("visually-hidden");
          $(e.target.parentNode).children("span").removeClass("spinner-border");
          $(e.target.parentNode)
            .closest(".card-body")
            .find(".text-bg-success")
            .first()
            .text(response.saves + " save");


        } else {
          $(e.target.parentNode).removeClass("text-warning");

          $(e.target.parentNode).children("svg").removeClass("visually-hidden");
          $(e.target.parentNode).children("span").removeClass("spinner-border");

          $(e.target.parentNode)
          .closest(".card-body")
          .find(".text-bg-success")
          .first()
          .text(response.saves + " save");
        }
      },
      error: function (xhr, status, error) {
        console.error("Error liking comment: " + error); // Error logging
      },
    });
  });

  likeCommentForm.submit(function (e) {
    e.preventDefault();

    $(e.target.parentNode).prop("disabled", true);
    $(e.target.parentNode).children("svg").addClass("visually-hidden");
    $(e.target.parentNode).children("span").addClass("spinner-border");

    const form = $(this);
    const url = form.attr("action"); // Get the action attribute from the form

    $.ajax({
      type: "POST",
      url: url,
      data: form.serialize(), // Serialize form data for submission
      success: function (response, status) {
        $(e.target.parentNode).prop("disabled", false);
        // update the UI
        if (response.action == "like") {
          $(e.target.parentNode).addClass("text-primary");

          $(e.target.parentNode).children("svg").removeClass("visually-hidden");
          $(e.target.parentNode).children("span").removeClass("spinner-border");
          $(e.target.parentNode)
          .closest(".card-body")
          .find(".text-bg-info")
          .first()
          .text(response.likes + " like");
        
        } else {
          $(e.target.parentNode).removeClass("text-primary");

          $(e.target.parentNode).children("svg").removeClass("visually-hidden");
          $(e.target.parentNode).children("span").removeClass("spinner-border");
          $(e.target.parentNode)
          .closest(".card-body")
          .find(".text-bg-info")
          .first()
          .text(response.likes + " like");
        }
      },
      error: function (xhr, status, error) {
        console.error("Error liking comment: " + error); // Error logging
      },
    });
  });
});
