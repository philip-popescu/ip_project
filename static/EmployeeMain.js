function roomsAvailable() {

    let from = document.getElementById("dateFrom");
    let to = document.getElementById("dateTo");

    let rez = {{rezervari}};
    let hotel_data = {{hotel_data}};

    const ids = [];

    for (let i in rez){
        if ( (from >= i.from && to <= i.to)
        || (to >= i.from && to <= i.to))
            ids.push(i.id);
    }

}