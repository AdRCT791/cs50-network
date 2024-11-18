document.addEventListener('DOMContentLoaded', function() {
    const textInput = document.getElementById('post-input-text');
    const charCountDisplay = document.getElementById('char-count-display');
    console.log(textInput);
    console.log(textInput.length);
    
    // Character count post input
    textInput.addEventListener('input', ()=>{
        const charCount = textInput.value.length;
        charCountDisplay.innerHTML = 300 - charCount;

        console.log(charCount);
    })

});
  
  