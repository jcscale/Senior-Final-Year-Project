a = "2022-04-07T18:01:07.221Z"

var now = new Date(a);
now.setSeconds(0, 0);
var stamp = now.toISOString().replace(/T/, " ").replace(/:00.000Z/, "");

console.log(stamp)

const date = new Date(stamp);
date.setSeconds(0, 0);

myTime = new Date(date).toLocaleTimeString();
console.log(typeof (myTime))

for (let element of myTime) {
    console.log(element.toLowerCase())
    if (element === 'A') {
        a = myTime.indexOf(element)
        myTime[a] = myTime[a].toLowerCase()
    }
}

console.log(a)
b = myTime.toLowerCase()
console.log(b)

function format(input) {
    var date = new Date(input.replace(/ /g, 'T'));
    return [
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"][date.getMonth()] + ' ' + date.getDate() + ', ' + date.getFullYear();
}



function convertTZ(date, tzString) {
    return new Date((typeof date === "string" ? new Date(date) : date).toLocaleString("en-US", { timeZone: tzString }));
}

// usage: Asia/Jakarta is GMT+7
console.log(convertTZ("2022-04-07T18:01:07.221Z", "Asia/Manila")) // Tue Apr 20 2012 17:10:30 GMT+0700 (Western Indonesia Time)

// Resulting value is regular Date() object
const convertedDatee = convertTZ("2022-04-07T18:01:07.221Z", "Asia/Manila")
console.log(convertedDatee.getHours()); // 17



// Bonus: You can also put Date object to first arg
const datee = new Date("2022-04-07T18:33:28.192Z")
datee.setSeconds(0, 0);
console.log(convertTZ(datee, "Asia/Manila")) // current date-time in jakarta.

abc = convertTZ(datee, "Asia/Manila")
console.log(abc.toTimeString())
myTimee = new Date(abc).toLocaleTimeString();

console.log(myTimee.toLowerCase())

result = myTimee.toLowerCase()
console.log(result.slice(0, 4))
console.log(result.slice(-2,))

stat = result.slice(-2,)
arr = []
for (let element of stat) {
    arr.push(element)
}
ampm = (arr.join(".") + ".")
// stat.splice(1, 0, ".")
// console.log(stat)

time = result.slice(0, 4)

petsa = format("2022-04-07T18:33:28.192Z")
console.log(petsa)

final = petsa + " " + time + " " + ampm

console.log(final)