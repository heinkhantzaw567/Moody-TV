// document.addEventListener("DOMContentLoaded",()=>{
//     const sumbit = document.querySelector('#loading')
//     sumbit.addEventListener('click', ()=>{
//         const mood = document.querySelector('#mood').innerHTML
//         const genre = document.querySelector('#genre').innerHTML
//         const Reason = document.querySelector('#Reason').innerHTML
//         const emotion = document.querySelector('#emotion').innerHTML
//         const data = {
//             mood: mood,
//             genre: genre,
//             reason: Reason,
//             emotion: emotion
//         };
//         fetch ('/home',{
//             method: 'POST',
//             headers:{
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify(data),
//         })
//         .then(response => response.json()) 
//         console.log(sumbit)
//     })
    
// })