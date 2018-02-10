alert("Step 0");
function readURL(input) {
    alert("step 1");

  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
        alert("step 2");
      $('#img').attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]);
  }
}

$("#pic").change(function() {
  readURL(this);
});
