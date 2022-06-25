function setup(){
    createCanvas(windowWidth/2, windowHeight);
    container = new Box(0, 0, windowWidth/2, windowHeight)
}

function draw() {
    // background(0, 255, 255);
    rect(container.x, container.y, container.a, container.b);
}

function windowResized() {
    resizeCanvas(windowWidth/2, windowHeight);
}

class Box{
    constructor(x, y, a, b){
        this.x = x;
        this.y = y;
        this.a = a;
        this.b = b;
    }
}