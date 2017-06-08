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

## Servos
````
[
    {
        id: int,
        readings: ServoInfo
    }
]
````

## Spider info
```
{
    battery: int,
    slope: float,
    cpuUsage: float,
    cpuTemperature: int
}
```
