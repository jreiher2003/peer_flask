function checkForm(form) // Submit button clicked
{
  form.submit.disabled = true;
  form.submit.value = "Please wait...";
  return true;
}
function OverUnder(form) // Submit button clicked
{
  form.submit_o.disabled = true;
  form.submit_o.value = "Please wait...";
  return true;
}
function AwaySideForm(form) // Submit button clicked
{
  form.submit_a.disabled = true;
  form.submit_a.value = "Please wait...";
  return true;
}
function HomeSideForm(form) // Submit button clicked
{
  form.submit_h.disabled = true;
  form.submit_h.value = "Please wait...";
  return true;
}
function CreateBitcoinForm(form)
{
  form.create.disabled = true;
  form.create.value = "Please wait...";
  return true;
}
function EditBet(form) 
{
  form.editbutton.disabled = true;
  form.editbutton.text = "Please wait..."
}