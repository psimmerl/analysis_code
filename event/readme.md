# CLAS12 Event Class
This class was designed to be a useful data structure to hold the CLAS12 detector information.  Each detector is represented in a map where the index of the particle in `REC::Particle` defines the map key.

### Simple Use
You can convert an entire `HipoDataEvent` using the `EventConverter.convert` method.

```groovy
def reader = HipoDataSource()
reader.open(filename)

while(reader.hasEvent()){
    def dataEvent = reader.getNextEvent()

    // This is where the conversion is done.
    def event = EventConverter.convert(dataEvent)
}

```

### Advanced Use
If you only need to check banks other than `REC::Particle` in a small fraction of your events, you can call the bank converters directly to increase the execution speed and reduce the memory usage of each event.  

```groovy
def reader = HipoDataSource()
reader.open(filename)

while(reader.hasEvent()){
    def dataEvent = reader.getNextEvent()

    def event = Event()
    EventConverter.convertScalar(dataEvent, event)
    EventConverter.convertPart(dataEvent, event)

    // Check something in REC::Particle and call other banks if needed. 

}

```

### Event Structure
The `Event` class contains detector information indexed by the index of the particle in `REC::Particle`.  Let's use the number of photoelectrons in the Cherenkov counter as an example.  Here, we select event builder electrons and get the number of photoelectrons. 

```groovy

(0 ..< event.npart).findAll{ index ->
   event.pid.get(index) == 11 
}.collect{ index ->
   event.nphe.get(index)
}

```

Please note that in groovy you can use the explicit map get as above, or the shorter notation `event.pid[index]`.  I have opted to use the first notation simply to re-enforce that the underlying data structure is a map. 

