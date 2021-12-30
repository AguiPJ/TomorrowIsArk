function fn(a,b){
    let c
   if(a>b)c=1
   if(a==b)c=0
   if(a<b)c=-1
   return c
}
var i =5
var a = fn(i,++i)
console.log(a);