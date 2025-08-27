#ifndef TEST_H
#define TEST_H

#include "example.h"

#pragma pack(1)

// 扩展宏定义
#define MAX_SECTORS 64
#define SECTOR_SIZE 512
#define MAX_PARTITIONS 4
#define DEVICE_NAME_LEN (64+MAX_PARTITIONS)
#define SERIAL_NUMBER_LEN 32

// 扩展的设备类型枚举
typedef enum
{
    DEVICE_TYPE_HDD = 0x01,
    DEVICE_TYPE_SSD = 0x02,
    DEVICE_TYPE_USB = 0x03,
    DEVICE_TYPE_SD = 0x04,
    DEVICE_TYPE_UNKNOWN = 0xFF
} DeviceType;

// 分区信息结构体
typedef struct
{
    unsigned char active : 1;  // 活动分区标志
    unsigned char type : 7;    // 分区类型
    unsigned int start_sector; // 起始扇区
    unsigned int sector_count; // 扇区数量
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
    char label[16]; // 分区标签
} PartitionInfo;

// 扇区统计信息
typedef struct
{
    unsigned long long total_sectors;
    unsigned long long used_sectors;
    unsigned long long bad_sectors;
    unsigned int sector_size;
    struct
    {
        double read_speed_mbps;   // 读取速度 MB/s
        double write_speed_mbps;  // 写入速度 MB/s
        unsigned int read_count;  // 读取次数
        unsigned int write_count; // 写入次数
        unsigned long long total_bytes_read;
        unsigned long long total_bytes_written;
    } performance;
} SectorStats;

// 设备健康状态
typedef struct
{
    unsigned short temperature;      // 温度 (摄氏度 * 10)
    unsigned char health_percentage; // 健康度百分比
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
    unsigned char error_log[32]; // 错误日志摘要
} DeviceHealth;

// 复杂的设备描述符结构体
typedef struct
{
    FileHeader header; // 使用 example.h 中的 FileHeader

    // 基本设备信息
    DeviceType device_type;
    char device_name[DEVICE_NAME_LEN];
    char serial_number[SERIAL_NUMBER_LEN];
    char firmware_version[16];

    // 物理特性
    struct
    {
        unsigned short cylinders;
        unsigned short heads;
        unsigned short sectors_per_track;
        unsigned int total_sectors;
    } geometry;

    // 分区表
    PartitionInfo partitions[MAX_PARTITIONS];
    unsigned char partition_count;

    // 性能和健康状态
    SectorStats stats;
    DeviceHealth health;

    // 高级特性位域
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

    // 嵌套的匿名结构体和联合体
    struct
    {
        union
        {
            struct
            {
                unsigned char interface_type : 4; // 接口类型 (SATA/USB/NVMe等)
                unsigned char connector_type : 4; // 连接器类型
            };
            unsigned char raw_interface;
        };

        struct
        {
            unsigned short vendor_id;
            unsigned short product_id;
            unsigned short revision;
        } ids;

        // 匿名联合体包含匿名结构体位域
        union
        {
            struct
            {
                unsigned char link_speed : 3;    // 链路速度等级
                unsigned char link_width : 3;    // 链路宽度
                unsigned char link_active : 1;   // 链路激活状态
                unsigned char link_training : 1; // 链路训练状态
            };
            unsigned char link_status;
        };
    } interface_info;

    // 缓存配置
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

    // 扩展属性数组
    struct
    {
        unsigned short attribute_id;
        unsigned int value;
        char description[32];
    } extended_attributes[16];

    // 固件更新信息
    struct
    {
        Version current_fw_version; // 重用 example.h 中的 Version
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

    // 安全特性
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

    // 预留空间和校验
    unsigned char reserved[64];
    unsigned int structure_checksum; // 整个结构体的校验和

} ComplexDeviceDescriptor;

// 设备管理器结构体 - 管理多个设备
typedef struct
{
    ComplexDeviceDescriptor devices[8];
    unsigned char device_count;

    // 全局统计
    struct
    {
        unsigned long long total_capacity_bytes;
        unsigned long long total_free_bytes;
        unsigned int total_read_operations;
        unsigned int total_write_operations;
        double average_response_time_ms;
    } global_stats;

    // 系统配置
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

    // 事件日志
    struct
    {
        unsigned int timestamp;
        unsigned char event_type;
        unsigned char device_index;
        unsigned short event_code;
        char description[64];
    } event_log[32];

    unsigned char log_count;
    FileHeader config_header; // 再次使用 FileHeader

} DeviceManager;

#endif // TEST_H
