# JSON Data 

## Angles
index is servo ID
```
[
    {
        id: int,
        angle, float
    }
]
```

## Servo info
```
{
    id: int,
    temperature: int,
    voltage: float,
    load: int,
    position: float
}
```

## Spider info
```
{
    battery: int,
    slope: float,
    cpuUsage: float,
    cpuTemperature: int
}
```

## Smart Controller info
Button map:
1: turn left
2: turn right
3: raise body
4: lower body
```
{
    joystick:{
        x: float,
        y: float
    },
    pressedButtons:int[]
}
```
