function checkForm(form) // Submit button clicked
{
  form.submit.disabled = true;
  form.submit.value = "Please wait...";
  return true;
}
function EditBet(form) 
{
  form.editbutton.disabled = true;
  form.editbutton.text = "Please wait..."
}