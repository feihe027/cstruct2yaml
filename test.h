#ifndef TEST_H
#define TEST_H

// PacketHeader struct for test and doc consistency
typedef struct
{
    unsigned char type : 4;
    unsigned char flags : 4;
    unsigned short length;
    unsigned int data[10];
} PacketHeader;

#include "example.h"

#pragma pack(1)

// Extended macro definitions
#define MAX_SECTORS 64
#define SECTOR_SIZE 512
#define MAX_PARTITIONS 4
#define DEVICE_NAME_LEN (64 + MAX_PARTITIONS)
#define SERIAL_NUMBER_LEN 32

// Extended device type enumeration
typedef enum
{
    DEVICE_TYPE_HDD = 0x01,
    DEVICE_TYPE_SSD = 0x02,
    DEVICE_TYPE_USB = 0x03,
    DEVICE_TYPE_SD = 0x04,
    DEVICE_TYPE_UNKNOWN = 0xFF
} DeviceType;

// Partition information structure
typedef struct
{
    unsigned char active : 1;  // Active partition flag
    unsigned char type : 7;    // Partition type
    unsigned int start_sector; // Start sector
    unsigned int sector_count; // Sector count
    union
    {
        struct
        {
            unsigned char readable : 1;
            unsigned char writable : 1;
            unsigned char bootable : 1;
            unsigned char system : 1;
            unsigned char hidden : 1;
            unsigned char reserved : 3;
        } flags;
        unsigned char raw_flags;
    };
    char label[16]; // Partition label
} PartitionInfo;

// Sector statistics
typedef struct
{
    unsigned long long total_sectors;
    unsigned long long used_sectors;
    unsigned long long bad_sectors;
    unsigned int sector_size;
    struct
    {
        double read_speed_mbps;   // Read speed MB/s
        double write_speed_mbps;  // Write speed MB/s
        unsigned int read_count;  // Read count
        unsigned int write_count; // Write count
        unsigned long long total_bytes_read;
        unsigned long long total_bytes_written;
    } performance;
} SectorStats;

// Device health status
typedef struct
{
    unsigned short temperature;      // Temperature (Celsius * 10)
    unsigned char health_percentage; // Health percentage
    union
    {
        struct
        {
            unsigned short power_on_hours : 16;
            unsigned short power_cycle_count : 16;
        };
        unsigned int raw_power_stats;
    };
    struct
    {
        unsigned char smart_available : 1;
        unsigned char smart_enabled : 1;
        unsigned char self_test_running : 1;
        unsigned char warning_temp : 1;
        unsigned char critical_temp : 1;
        unsigned char failure_predicted : 1;
        unsigned char reserved : 2;
    } status;
    unsigned char error_log[32]; // Error log summary
} DeviceHealth;

// Complex device descriptor structure
typedef struct
{
    FileHeader header; // Using FileHeader from example.h

    // Basic device information
    DeviceType device_type;
    char device_name[DEVICE_NAME_LEN];
    char serial_number[SERIAL_NUMBER_LEN];
    char firmware_version[16];

    // Physical characteristics
    struct
    {
        unsigned short cylinders;
        unsigned short heads;
        unsigned short sectors_per_track;
        unsigned int total_sectors;
    } geometry;

    // Partition table
    PartitionInfo partitions[MAX_PARTITIONS];
    unsigned char partition_count;

    // Performance and health status
    SectorStats stats;
    DeviceHealth health;

    // Advanced feature bit fields
    union
    {
        struct
        {
            unsigned int trim_supported : 1;
            unsigned int encryption_supported : 1;
            unsigned int smart_supported : 1;
            unsigned int lba48_supported : 1;
            unsigned int dma_supported : 1;
            unsigned int ncq_supported : 1;
            unsigned int hotplug_supported : 1;
            unsigned int power_management : 1;
            unsigned int write_cache_enabled : 1;
            unsigned int read_cache_enabled : 1;
            unsigned int reserved : 22;
        } features;
        unsigned int raw_features;
    };

    // Nested anonymous structures and unions
    struct
    {
        union
        {
            struct
            {
                unsigned char interface_type : 4; // Interface type (SATA/USB/NVMe, etc.)
                unsigned char connector_type : 4; // Connector type
            };
            unsigned char raw_interface;
        };

        struct
        {
            unsigned short vendor_id;
            unsigned short product_id;
            unsigned short revision;
        } ids;

        // Anonymous union containing anonymous structure bit fields
        union
        {
            struct
            {
                unsigned char link_speed : 3;    // Link speed level
                unsigned char link_width : 3;    // Link width
                unsigned char link_active : 1;   // Link active status
                unsigned char link_training : 1; // Link training status
            };
            unsigned char link_status;
        };
    } interface_info;

    // Cache configuration
    struct
    {
        unsigned int cache_size_kb;
        union
        {
            struct
            {
                unsigned char write_through : 1;
                unsigned char write_back : 1;
                unsigned char read_ahead : 1;
                unsigned char adaptive : 1;
                unsigned char flush_capable : 1;
                unsigned char reserved : 3;
            } cache_flags;
            unsigned char raw_cache_flags;
        };
        unsigned short cache_line_size;
    } cache_config;

    // Extended attribute array
    struct
    {
        unsigned short attribute_id;
        unsigned int value;
        char description[32];
    } extended_attributes[16];

    // Firmware update information
    struct
    {
        Version current_fw_version; // Reuse Version from example.h
        Version latest_fw_version;
        union
        {
            struct
            {
                unsigned char update_available : 1;
                unsigned char update_critical : 1;
                unsigned char update_in_progress : 1;
                unsigned char rollback_available : 1;
                unsigned char reserved : 4;
            } update_flags;
            unsigned char raw_update_flags;
        };
        char update_url[128];
        unsigned int update_size_bytes;
    } firmware_info;

    // Security features
    struct
    {
        union
        {
            struct
            {
                unsigned char password_enabled : 1;
                unsigned char encryption_enabled : 1;
                unsigned char secure_erase_supported : 1;
                unsigned char master_password_capability : 1;
                unsigned char user_password_capability : 1;
                unsigned char frozen : 1;
                unsigned char locked : 1;
                unsigned char security_enabled : 1;
            } security_flags;
            unsigned char raw_security_flags;
        };
        unsigned char password_hash[32];
        unsigned int unlock_count;
        unsigned int failed_unlock_count;
    } security;

    // Reserved space and checksum
    unsigned char reserved[64];
    unsigned int structure_checksum; // Checksum for the entire structure

} ComplexDeviceDescriptor;

// Device manager structure - manages multiple devices
typedef struct
{
    ComplexDeviceDescriptor devices[8];
    unsigned char device_count;

    // Global statistics
    struct
    {
        unsigned long long total_capacity_bytes;
        unsigned long long total_free_bytes;
        unsigned int total_read_operations;
        unsigned int total_write_operations;
        double average_response_time_ms;
    } global_stats;

    // System configuration
    union
    {
        struct
        {
            unsigned char auto_mount : 1;
            unsigned char auto_scan : 1;
            unsigned char power_save_mode : 1;
            unsigned char hot_swap_enabled : 1;
            unsigned char raid_enabled : 1;
            unsigned char compression_enabled : 1;
            unsigned char encryption_required : 1;
            unsigned char reserved : 1;
        } system_flags;
        unsigned char raw_system_flags;
    };

    // Event log
    struct
    {
        unsigned int timestamp;
        unsigned char event_type;
        unsigned char device_index;
        unsigned short event_code;
        char description[2][64];
    } event_log[32];

    unsigned char log_count;
    FileHeader config_header; // Using FileHeader again

} DeviceManager;

#endif // TEST_H
