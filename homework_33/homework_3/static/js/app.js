function hello()
{
    uName = document.getElementById("name").value;
    document.getElementById("helloName").innerText = `Доброго времени суток, ${uName}, 
    здесь вы можете оставить своё сообщение`;
}


function send()
{
    message = document.getElementById("message").value;
    document.getElementById("sendMessage").value = '';
    (async () => 
    {
        var response = await fetch("chat.php?message=" + message);
        var answer = await response.text();

    }
)();
}

function get() 
{
    (async () => 
    {
        var response = await fetch("chat.php");
        var answer = await response.text();
        document.getElementById("sendMessage").innerText = answer;
    }
)();
}

get();

setInterval(get, 2000);