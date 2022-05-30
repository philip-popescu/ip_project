function roomsAvailable() {

    let from = document.getElementById("dateFrom");
    let to = document.getElementById("dateTo");

    let rez = {{rezervari}};
    let hotel_data = {{hotel_data}};

    const no_ids = [];
    const yes_ids = [];

    for (let i in rez){
        if ( (from >= i.from && to <= i.to)
        || (to >= i.from && to <= i.to))
            no_ids.push(i.room_id);
    }

    for (let j in hotel_data) {
        if( !no_ids.includes(j.rooms[0]))
            yes_ids.push(j.rooms);
    }

    return yes_ids;
}