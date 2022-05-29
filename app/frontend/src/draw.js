import Sketch from 'react-p5'


const setup = (p5, canvasParentRef) => {
    p5.createCanvas(1225, 1225).parent(canvasParentRef)
}

const draw = p5 => {
    p5.background(255, 130, 20)
    p5.ellipse(100, 100, 100)
    p5.ellipse(300, 100, 100)
}

export default { setup, draw }