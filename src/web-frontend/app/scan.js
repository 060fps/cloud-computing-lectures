window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://front-end-student-milena-mihajlovic.mycluster-eu-de-1-244439-975dd9665934b81fa7342475b7855171-0000.eu-de.containers.appdomain.cloud");
  
    document.querySelector(".minus").addEventListener("click", () => {
      websocket.send(JSON.stringify({ action: "minus" }));
    });
  
    document.querySelector(".plus").addEventListener("click", () => {
      websocket.send(JSON.stringify({ action: "plus" }));
    });
  
    websocket.onmessage = ({ data }) => {
      const event = JSON.parse(data);
      switch (event.type) {
        case "value":
          document.querySelector(".value").textContent = event.value;
          break;
        case "users":
          const users = `${event.count} user${event.count == 1 ? "" : "s"}`;
          document.querySelector(".users").textContent = users;
          break;
        default:
          console.error("unsupported event", event);
      }
    };
  });
