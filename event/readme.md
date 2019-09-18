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


