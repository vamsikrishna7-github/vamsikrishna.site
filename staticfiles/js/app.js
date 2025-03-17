// loading Animation
window.addEventListener('load', function() {
    // console.log('Page fully loaded'); 
    document.getElementById('loading').style.display = 'none';
  });

window.addEventListener('resize', resize);

function resize() {
    // console.log('resize:', window.innerWidth);
}

resize();
// console.log('Hello');

// about section
function knowmore(link) {
    const moreInfo = document.querySelector('.display-text');
    
    if (!moreInfo.classList.contains('show')) {
        moreInfo.classList.add('show');
        link.innerHTML = "Read less";
    } else {
        moreInfo.classList.remove('show');
        link.innerHTML = "Know more";
    }
}

// contact section form
function validateEmail(input) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const submit = document.querySelector('#submit');
    
    input.classList.remove('border-secondary', 'border-danger', 'border-success');

    if (!emailPattern.test(input.value.trim())) {
        input.classList.add('border-danger');
        submit.classList.add('disabled');
    } else {
        input.classList.add('border-success');
        submit.classList.remove('disabled');
    }
}

// global view all 
function viewAll(link) {
    const services = document.querySelectorAll('.show-hide');
    const imgSrc = link.getAttribute('data-viewall-img');

    if (!link.classList.contains('active')) {
        link.classList.add('active');
        services.forEach(service => {
            service.classList.add('active');
            service.style.display = "block"; 
        });
        link.innerHTML = `View less <img width='20' height='20' src='${imgSrc}' alt='show-all-views'/>`;
    } else {
        link.classList.remove('active');
        services.forEach(service => {
            service.classList.remove('active'); 
            setTimeout(() => {
                service.style.display = "none"; 
            }, 500); 
        });
        link.innerHTML = `View all <img width='20' height='20' src='${imgSrc}' alt='show-all-views'/>`;
    }
}

// projects
function projectsViewAll(link) {
    const projects = document.querySelector('.show-hide-projects');
    const imgSrc = link.getAttribute('data-viewall-img'); 

    if (!projects.classList.contains('d-none')) {
        projects.classList.add('d-none');
        link.innerHTML = `View all <img width='20' height='20' src='${imgSrc}' alt='show-all-views'/>`;
    } else {
        projects.classList.remove('d-none');
        link.innerHTML = `View less <img width='20' height='20' src='${imgSrc}' alt='show-all-views'/>`;
    }
}


// responsive nav-bar
let homelink;
function activelink(){
    const sections = document.querySelectorAll('section');
    const links = document.querySelectorAll('.nav-link');
    homelink = document.getElementsByName('home')[0];
    sections.forEach(section => {
    const rect = section.getBoundingClientRect();
    if (rect.top <= window.innerHeight / 2 && rect.bottom >= window.innerHeight / 2) {
        // console.log(`Section ${section.id} is in view.`);
        links.forEach(link => {
            if(link.name === section.id){
                link.classList.add('active');
                if(homelink) homelink.classList.remove('active');
            }
        });
       } else {
         links.forEach(link => {
            if(link.name === section.id){
                if(section.id === 'projects'){
                    if(homelink) homelink.classList.add('active');
                }
                link.classList.remove('active');
            }
         });
        }
   });
}

window.addEventListener('scroll', activelink);

//scrole to top
function scrollToTop(btn) {
    window.scrollTo({ top: 0, behavior:'smooth' });
}

window.addEventListener('scroll', toggleScrollButton);
window.addEventListener('DOMContentLoaded', toggleScrollButton);

function toggleScrollButton() {
    const btn = document.querySelector('#scrollToTopBtn');
    if (window.scrollY > 100) {
        btn.classList.remove('d-none');
    } else {
        btn.classList.add('d-none');
    }
}
