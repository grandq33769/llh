var num = 12;
const str = 'Mark';

//Local Variable
function checkLike() {
    let isActived = true;
}

console.log(num);
console.log(str);
// console.log(isActived)

//Reference Data Type
let a = {
    name: 'Zuck'
};
console.log(a);
let b = a;
b.name = 'Jack';
console.log(a);

//Operator
const name = 'Mark';
const sum = 1 + 3;
const age = 23;
// const canVote = age >= 20;
const canVote = age < 20;
console.log(canVote);

const c = true;
const d = false;
const result1 = c && d;
const result2 = c || d;
console.log(result1);
console.log(result2);

//Flow control
//if
if (age > 20) {
    console.log('Can Vote !');
}

//switch
const country = 'Taiwan';
switch (country) {
    case 'Taiwan':
        console.log('hello tw !');
    case 'Japan':
        console.log('hello jp ~');
    case 'Korea':
        console.log('hello kn ~~');
    default:
        console.log('hello' + country);
}

//for
const arr = ['Mark', 'Zuck', 'Jack'];
for (let i = 0; i < arr.length; i++) {
    console.log(arr[i]);
}

//while
var num2 = 1;
let sum2 = 0;
while (num2 <= 10) {
    sum2 += num2;
    num2 += 1;
    console.log(sum2);
}

//do ... while
let x = 0;
while (x < 10) {
    console.log(x);
    x++;
}

let y = 0;
do {
    console.log(y);
    y++;
} while (y < 0);

//function
const sum_func = (x, y) => {
    return x + y;
};
console.log(sum_func(1, 3));

//object
var obj = new Object();
console.log(obj);

var obj = {
    name: 'Mark',
    age: 23
}
console.log(obj);

function Dog(name, age) {
    this.name = name;
    this.age = age;
    this.wow = () => {
        console.log('wow!wow');
    }
}

Dog.prototype.cry = () => {
    console.log('QQ');
}

const dog = new Dog('Lucky', 2);
dog.wow();
dog.cry();