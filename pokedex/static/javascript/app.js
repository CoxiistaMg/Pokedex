const num_cov = [
    'I',
    'II',
    'III',
    'IV',
    'V',
    'VI',
    'VII',
    'VIII'
]

   const num_gen = [
   'yellow', 
   'crystal', 
   'firered-leafgreen', 
   'heartgold-soulsilver', 
   'black-2-white-2',
   'x-y',
   'ultra-sun-ultra-moon', 
   'sword-shield'
    
  ]

var moves_level = {}
var moves_egg = {}
var moves_tutor = {}
var moves_tm = {}
var moves_tr = {}
var moves_tr_over_100 = {}
var moves_tm_over_100 = {}

for (each in poke_moves){
  document.getElementById(`gen-button-number`).innerHTML += `<button onclick='change_moves(${each})' class="btn btn-dark mt-4 ml-5">${num_cov[each]}</button>`
}

for (i in poke_moves){
    moves_level[i] = {}
    moves_tutor[i] = []
    moves_egg[i] = []
    moves_tm[i] = {}
    moves_tr[i] = {}
    moves_tr_over_100[i] = {}
    moves_tm_over_100[i] = {}

    for (each of poke_moves[i]){
        method = each[0]
        level = each[1]
        number_mov = each[2]

        if (each[0] == 3){        
            tms_ = tms[i][number_mov]
       
            if (tms_.includes('tr')){
                if (parseInt(tms_.replace('tr', '')) >= 100){
                    moves_tr_over_100[i][tms_] = number_mov
                    
                }
                else{moves_tr[i][tms_] = number_mov}
            }

            else{
                if (parseInt(tms_.replace('tm', '')) >= 100){
                    moves_tm_over_100[i][tms_] = number_mov
                }
                else{
                    moves_tm[i][tms_] = number_mov

            }
        }
        }

        else if (each[0] == 0){
            moves_egg[i].push(each[2])
        }

        else if (each[0] == 2){
            moves_tutor[i].push(each[2])
        }

        else {
            if (each[1] != 0){
            if (!Object.keys(moves_level[i]).includes(each[1].toString())){
                moves_level[i][each[1]] = []
            }
            moves_level[i][each[1]].push(each[2])}
        
        }
    }
}


function change_moves(e){

  document.getElementById('level').innerHTML  = ''
  document.getElementById('tm/tr').innerHTML  = ''
  document.getElementById('egg_table').innerHTML  = ''
  document.getElementById('tutor_table').innerHTML  = ''

  document.getElementById('current_gen').innerHTML  = num_cov[e]

  for (i in moves_level[e]){
    for (each of moves_level[e][i]){
        move = moves[each-1]
        title = move[0].replace('-', ' ')
        document.getElementById('level').innerHTML += `
                <td>${i}</td>
                <td class='text-center'>${title}</td>
                <td class='text-center'>${move[2]}</td>
                <td>${move[1]}</td>
                <td>${move[3]}</td>
                <td><img src="/media/types/${move[6]}.jpg" class='img-fluid' alt="" srcset=""></td>
                <td>${move[4]}</td>
            
            
            `
    }}

  for (each of Object.keys(moves_tm[e]).sort()){
    tm = moves_tm[e][each]
    move = moves[tm-1]
    name = move[0].replace('-', ' ')
    document.getElementById('tm/tr').innerHTML += `
            <td>${each}</td>
            <td class='text-center'>${name}</td>
            <td class='text-center'>${move[2]}</td>
            <td>${move[1]}</td>
            <td>${move[3]}</td>
            <td><img src="/media/types/${move[6]}.jpg" class='img-fluid' alt="" srcset=""></td>
            <td>${move[4]}</td>
           
          
        `
  }

  if (moves_egg[e].length != 0){
    info = ''
    for (each of moves_egg[e]){
        move = moves[each-1]
        title = move[0].replace('-', ' ')
        info += `
        <tr>
        <td>${title}</td>
        <td class='text-center'>${move[2]}</td>
        <td>${move[1]}</td>
        <td>${move[3]}</td>
        <td><img src="/media/types/${move[6]}.jpg" class='img-fluid' alt="" srcset=""></td>
        <td>${move[4]}</td>
        <tr>
        `
    }
    document.getElementById('egg_table').innerHTML = `<table class="table">
              <h3>Moves learnt by Egg</h3>
                <thead>
                  <tr>
                    <th style="width: 240px;" class="col">Move</th>
                    <th style="width: 64px;" class="col">Power</th>
                    <th class="col text-center">ACC.</th>
                    <th class="col text-center">PP</th>
                    <th style="width: 64px;">Type</th>
                    <th style="width: 64px;">Cat.</th>
                  </tr>
                </thead>
                <tbody>
                 ${info}
                  <tr>
                </tr>
                </tbody>
              </table>`
}


if (moves_tutor[e].length != 0){
    info = ''
    for (each of moves_tutor[e]){
        move = moves[each-1]
        title = move[0].replace('-', ' ')
        info += `
        <tr>
        <td>${title}</td>
        <td class='text-center'>${move[2]}</td>
        <td>${move[1]}</td>
        <td>${move[3]}</td>
        <td><img src="/media/types/${move[6]}.jpg" class='img-fluid' alt="" srcset=""></td>
        <td>${move[4]}</td>
        <tr>
        `
    }
    document.getElementById('tutor_table').innerHTML = `<table class="table">
              <h3>Moves learnt by Tutor</h3>
                <thead>
                  <tr>
                    <th style="width: 240px;" class="col">Move</th>
                    <th style="width: 64px;" class="col">Power</th>
                    <th class="col text-center">ACC.</th>
                    <th class="col text-center">PP</th>
                    <th style="width: 64px;">Type</th>
                    <th style="width: 64px;">Cat.</th>
                  </tr>
                </thead>
                <tbody>
                 ${info}
                  <tr>
                </tr>
                </tbody>
              </table>`
}}
  i = Object.keys(poke_moves).length 
  i = Object.keys(poke_moves)[i-1]

  change_moves(i)