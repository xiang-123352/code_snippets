#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdarg.h>
#include <libusb-1.0/libusb.h>


/********************************************************************************
 * DEFINITION OF CONSTANTS AND STRUCTURES
 ********************************************************************************/
#define USB_PKT_SIZE                64
#define YOCTO_SERIAL_LEN            20
#define YOCTO_VENDORID              0x24e0
#define YOCTO_DEBUG_DEVID           0x99


#pragma pack(push,1)

/*
 * OUR USB PACKET FORMAT:
 * we always transmit 64 bytes
 */
typedef union {
    uint8_t              data[USB_PKT_SIZE];
    uint16_t             data16[USB_PKT_SIZE/2];
    uint32_t             data32[USB_PKT_SIZE/4]; 
} USB_Packet;

#pragma pack(pop)


typedef struct {
    unsigned                 endp;
    USB_Packet               pkt;
} ENDPOINT;

typedef struct {
    unsigned                cmd_sent;
    unsigned                vendorid;
    unsigned                deviceid;
    unsigned                ifaceno;
    char                    serial[YOCTO_SERIAL_LEN*2];

    libusb_device           *devref;
    libusb_device_handle    *hdl;

    ENDPOINT                 rd;
    ENDPOINT                 wr;
} yInterfaceSt;


/********************************************************************************
  FATAL_ERROR MACRO + function : all error will be reported with this function
 ********************************************************************************/

#define FATAL_ERROR(fmt,args...) fatal_error(__LINE__,fmt, ## args)
static void fatal_error(int line,const char *fmt,...)
{
    va_list args;

    printf("FATAL_ERROR ON LINE %d\n",line);
    va_start( args, fmt );
    vprintf(fmt,args);
    va_end(args);

#if 1
    // never ending loop to be able to break into GDB
    // and have stack frame
    while (1) {
        // INSERT YOUR GDB BREAKPOINT HERE
        sleep(1);
    }
#endif

    return;
}


/*****************************************************************************
  macro:
    PrintLibUSBErr(constchar * message)

  Summary:
    Will display an decoded libusb error.

  Note:
    This function will call fatal_error and never return, in order to 
    break into gdb

  ***************************************************************************/

#define PrintLibUSBErr(err,errmsg)  PrintLibUSBErrEx(__LINE__,err,errmsg)
static void PrintLibUSBErrEx(unsigned line,int err,char *intro_msg)
{
    char *msg;
    switch(err){
        case LIBUSB_SUCCESS:            msg="Success (no error)";break;
        case LIBUSB_ERROR_IO:           msg="Input/output error"; break;
        case LIBUSB_ERROR_INVALID_PARAM:msg="Invalid parameter"; break;
        case LIBUSB_ERROR_ACCESS:       msg="Access denied (insufficient permissions)"; break;
        case LIBUSB_ERROR_NO_DEVICE:    msg="No such device (it may have been disconnected)"; break;
        case LIBUSB_ERROR_NOT_FOUND:    msg="Entity not found"; break;
        case LIBUSB_ERROR_BUSY:         msg="Resource busy"; break;
        case LIBUSB_ERROR_TIMEOUT:      msg="Operation timed out"; break;
        case LIBUSB_ERROR_OVERFLOW:     msg="Overflow"; break;
        case LIBUSB_ERROR_PIPE:         msg="Pipe error"; break;
        case LIBUSB_ERROR_INTERRUPTED:  msg="System call interrupted (perhaps due to signal)"; break;
        case LIBUSB_ERROR_NO_MEM:       msg="Insufficient memory"; break;
        case LIBUSB_ERROR_NOT_SUPPORTED:msg="Operation not supported or unimplemented on this platform"; break;
        default:
        case LIBUSB_ERROR_OTHER:        msg="Other error"; break;
    }
    fatal_error(line,"libusb-1.0 error: %s / %s",intro_msg,msg);
};



/*****************************************************************************
  function:
    int getUsbStringASCII(libusb_device_handle *dev, int desc_index, char *data, unsigned length)

  Summary:
    helper to get the serial of an USB device into ASCII

  ***************************************************************************/
static int getUsbStringASCII(libusb_device_handle *dev, int desc_index, char *data, unsigned length)
{   
    unsigned char  buffer[512];
    unsigned l,len;
    int res;

    res=libusb_control_transfer(dev, LIBUSB_ENDPOINT_IN,
        LIBUSB_REQUEST_GET_DESCRIPTOR, (LIBUSB_DT_STRING << 8) | desc_index,
        0, buffer, 512, 10000);
    if(res<0) return res;

    len=(buffer[0]-2)/2;
    for(l=0;l<len && l<length;l++){
        data[l] = buffer[2+(l*2)];
    }
    
    return len;
}


/*****************************************************************************
  function:
    static int findDevice(libusb_context *libusb_ctx, yInterfaceSt  *iface)

  Summary:
    Will find the first Yoctopuce device with the debug firmware and init the
    yInterfaceSt structure in argument with the information of the devices

  Return:
    -1 on error;
    0  if Yoctopuce debug device are detected
    1  if everything went well

  ***************************************************************************/
static int findDevice(libusb_context *libusb_ctx, yInterfaceSt  *iface)
{
    libusb_device   **list;
    ssize_t         nbdev;
    int             i,res=0;
    
    // get all devices list
    nbdev=libusb_get_device_list(libusb_ctx,&list);
    if(nbdev<0){
        PrintLibUSBErr(nbdev,"libusb_get_device_list");
        return -1;
    }
    printf("%d USB devices found\n",(int)nbdev);


    for(i=0; i < nbdev; i++){
        struct libusb_device_descriptor desc;
        
        libusb_device  *dev=list[i];
        if((res=libusb_get_device_descriptor(dev,&desc))!=0){
            PrintLibUSBErr(res,"libusb_get_device_descriptor");
            return -1;
        }
        printf("device %x:%x\n",desc.idVendor,desc.idProduct);                    
        if(desc.idVendor!=YOCTO_VENDORID || desc.idProduct!=YOCTO_DEBUG_DEVID){
            continue;
        }
        printf("Use device %x:%x\n",desc.idVendor,desc.idProduct);                    


        res = libusb_open(dev,&iface->hdl);
        if(res==LIBUSB_ERROR_ACCESS){
            printf("the user has insufficient permissions to access USB devices\n");
            return -1;
        } 
        if(res!=0){
            printf("unable to access device %x:%x\n",desc.idVendor,desc.idProduct);
            continue;                
        }
        printf("try to get serial for %x:%x:%x\n",desc.idVendor,desc.idProduct,desc.iSerialNumber);
        
        iface->vendorid=desc.idVendor;
        iface->deviceid=desc.idProduct;
        res = getUsbStringASCII(iface->hdl,desc.iSerialNumber,iface->serial,YOCTO_SERIAL_LEN);              
        if(res<0){
            printf("unable to get serial for device %x:%x\n",desc.idVendor,desc.idProduct);                                
        }
        printf("----Running Dev %x:%x:%d:%s ---\n",desc.idVendor,desc.idProduct,0,iface->serial);
        iface->devref   = libusb_ref_device(dev);
        res = 1;
        break;
    }
    libusb_free_device_list(list,1);
    return res;
}




/*****************************************************************************  
  Summary:
    this small debug program will search for an Yoctopuce device with a debug
    firmware and start a burst transfer of 4096 packet of 64 bytes. 
    see README for more informations
  ***************************************************************************/
int main(int argc, const char* argv[])
{
    int             res, i, transfered, pktdrop;
    yInterfaceSt    iface;  
    unsigned        Nb_packet_To_receive;
    unsigned        Packet_Number;


    // LIBUSB-1.0 variables and pointers
    libusb_context                              *libusb_ctx;
    struct libusb_config_descriptor             *config;
    const struct libusb_interface_descriptor    *ifd;

    // init libusb-1.0
    res =libusb_init(&libusb_ctx);
    if(res!=0){
        PrintLibUSBErr(res,"libusb_init");
        return 1;
    }
    // activate debug (in most case this do nothing
    // because shared libraries are compiled without 
    // debug activated)
    libusb_set_debug(libusb_ctx,3);

    // clear our struct
    memset(&iface,0,sizeof(iface));

    // search for an Yoctopuce Device with the debug firmware
    // if we found an matching device the iface var will be updated
    // with correct informations
    printf("Search for Yoctopuce devices with debug firmware\n");
    res =findDevice(libusb_ctx,&iface);
    if (res==0) {
        printf("No Yoctopuce devices with debug firmware detected\n");
        return 1;
    } else if (res <0) {
        printf("Error during enumeration\n");
        return 1;
    }

    printf("Check that the kernel has no lock the device\n");
    if((res=libusb_kernel_driver_active(iface.hdl,0))<0){
        PrintLibUSBErr(res,"libusb_kernel_driver_active");   
        return 1;
    }
    if(res){
        printf("%s need to detach kernel driver\n",iface.serial);
        if((res = libusb_detach_kernel_driver(iface.hdl,0))<0){
            PrintLibUSBErr(res,"libusb_detach_kernel_driver");   
            return 1;
        }
    }

    printf("Claim interface of %s\n",iface.serial);
    if((res = libusb_claim_interface(iface.hdl,0))<0){
        PrintLibUSBErr(res,"libusb_claim_interface");   
        return 1;
    }


    printf("Get Active Configuration\n");
    res = libusb_get_active_config_descriptor(iface.devref,  &config);
    if(res==LIBUSB_ERROR_NOT_FOUND){
        printf("WARNING:Not yet configured -> use the configuration 0\n");
        if((res=libusb_get_config_descriptor(iface.devref, 0, &config))<0){
            PrintLibUSBErr(res,"libusb_get_config_descriptor");   
            return 1;
        }
    }else if(res!=0){
        PrintLibUSBErr(res,"unable to get active configuration %d");   
        return 1;
    }

    // find endpoint for interface 0
    ifd = &config->interface[0].altsetting[0];
    for (i = 0; i < ifd->bNumEndpoints; i++) {
        printf("endpoint %X size=%d \n",ifd->endpoint[i].bEndpointAddress,ifd->endpoint[i].wMaxPacketSize);
        if((ifd->endpoint[i].bEndpointAddress & LIBUSB_ENDPOINT_DIR_MASK) == LIBUSB_ENDPOINT_IN){
            iface.rd.endp = ifd->endpoint[i].bEndpointAddress;
        }else{
            iface.wr.endp = ifd->endpoint[i].bEndpointAddress;            
        }         
    }



    printf("Drop any packet of potential previous run\n");
    pktdrop=0;
    while (1) {
        int readed;

        res = libusb_interrupt_transfer(    iface.hdl,
                                            iface.rd.endp,
                                            (unsigned char *)&iface.rd.pkt,
                                            sizeof(USB_Packet),
                                            &readed,
                                            500);
        if(res ==  LIBUSB_ERROR_TIMEOUT ){
            //timeout -> no more packet all queue are clean
            break;
        }
        if(res<0){
            PrintLibUSBErr(res,"libusb_interrupt_transfer (read)");
            return 1;
        }
        pktdrop++;
    }
    printf("we have drop %d packets\n",pktdrop);
    sleep(1);// sleep a bit to help to identify burst in USB capture


    // Start a burst transfer
    Nb_packet_To_receive = 4096;
    Packet_Number = 3; 


    printf("Test a burst of 0x%X packet form 0x%X to 0x%X\n", 
        Nb_packet_To_receive , Packet_Number , Packet_Number + Nb_packet_To_receive);
    iface.wr.pkt.data32[0] = Packet_Number;
    iface.wr.pkt.data32[1] = Nb_packet_To_receive;
    printf("Send start to the device\n");
    res = libusb_interrupt_transfer(iface.hdl,
        iface.wr.endp,
        (unsigned char *)&iface.wr.pkt,
        sizeof(USB_Packet),
        &transfered,
        5000);
    if(res<0){
        PrintLibUSBErr(res,"libusb_interrupt_transfer");        
        return 1;
    }
    if(transfered != sizeof(USB_Packet)){
        printf("Incomplete host 2 device libusb_interrupt_transfer\n");
    }
  


    while (Nb_packet_To_receive) {
        int readed;

        res = libusb_interrupt_transfer(    iface.hdl,
                                            iface.rd.endp,
                                            (unsigned char *)&iface.rd.pkt,
                                            sizeof(USB_Packet),
                                            &readed,
                                            0);
        if(res<0){
            PrintLibUSBErr(res,"libusb_interrupt_transfer (read)");
            return 1;
        }
        printf("pkt_arrived (pkno=0x%X len=%d)\n",iface.rd.pkt.data32[0], readed);
        if (Nb_packet_To_receive==0){
            FATAL_ERROR("Unexpected packet received (%d)\n",Nb_packet_To_receive);
        }
        if (iface.rd.pkt.data32[0] != Packet_Number) {
            FATAL_ERROR("missing packet (expected = 0x%X  received = 0x%X)\n",Packet_Number,iface.rd.pkt.data32[0] );
        }
        Packet_Number++;
        Nb_packet_To_receive--;
    }

    printf("Everything went Well. Clean-up things\n");
    libusb_close(iface.hdl);
    libusb_exit(libusb_ctx);
    return 0;
}

