 window.onload = function() {
            const loadbg = document.querySelector(".loadbg");
            const loading = document.querySelector(".loading");


            loadbg.classList.add("loadbged");

            setTimeout(() => {
                loadbg.remove();
                loading.remove();
            }, 100);
        }