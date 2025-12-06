import psutil

def get_mounted_disks():
    """
    获取所有挂载的硬盘信息
    返回格式：字典列表，每个字典包含一个挂载点的信息
    """
    disks_info = []
    
    # 获取所有磁盘分区信息
    partitions = psutil.disk_partitions(all=False)  # all=False 只返回物理设备
    
    for partition in partitions:
        try:
            # 获取磁盘使用情况
            usage = psutil.disk_usage(partition.mountpoint)
            
            disk_info = {
                'device': partition.device,          # 设备路径
                'mountpoint': partition.mountpoint,  # 挂载点
                'fstype': partition.fstype,          # 文件系统类型
                'opts': partition.opts,              # 挂载选项
                'total_gb': round(usage.total / (1024**3), 2),     # 总容量(GB)
                'used_gb': round(usage.used / (1024**3), 2),       # 已用容量(GB)
                'free_gb': round(usage.free / (1024**3), 2),       # 可用容量(GB)
                'percent': usage.percent,            # 使用百分比
                'total_bytes': usage.total,          # 总容量(字节)
                'used_bytes': usage.used,            # 已用容量(字节)
                'free_bytes': usage.free             # 可用容量(字节)
            }
            
            disks_info.append(disk_info)
            
        except (PermissionError, OSError):
            # 跳过无法访问的分区（如光驱、没有权限的挂载点等）
            continue
    
    return disks_info

def get_mounted_disks_dict():
    """
    获取所有挂载的硬盘信息
    返回格式：以挂载点为键的字典
    """
    result = {}
    disks_list = get_mounted_disks()
    
    for disk in disks_list:
        result[disk['mountpoint']] = disk
    
    return result

def get_disk_usage_summary():
    """
    获取磁盘使用情况摘要
    """
    disks = get_mounted_disks()
    summary = {
        'total_disks': len(disks),
        'total_capacity_gb': round(sum(d['total_gb'] for d in disks), 2),
        'total_used_gb': round(sum(d['used_gb'] for d in disks), 2),
        'total_free_gb': round(sum(d['free_gb'] for d in disks), 2),
        'disks': disks
    }
    return summary

if __name__ == "__main__":
    # 示例用法
    
    print("=== 所有挂载磁盘信息（列表格式）===")
    disks_list = get_mounted_disks()
    print(disks_list)
    for i, disk in enumerate(disks_list, 1):
        print(f"\n磁盘 #{i}:")
        print(f"  设备: {disk['device']}")
        print(f"  挂载点: {disk['mountpoint']}")
        print(f"  文件系统: {disk['fstype']}")
        print(f"  总容量: {disk['total_gb']} GB")
        print(f"  已用: {disk['used_gb']} GB ({disk['percent']}%)")
        print(f"  可用: {disk['free_gb']} GB")
    
    print("\n=== 所有挂载磁盘信息（字典格式）===")
    disks_dict = get_mounted_disks_dict()
    for mountpoint, info in disks_dict.items():
        print(f"{mountpoint}: {info['total_gb']} GB, {info['percent']}% 已用")
    
    print("\n=== 磁盘使用情况摘要 ===")
    summary = get_disk_usage_summary()
    print(f"磁盘总数: {summary['total_disks']}")
    print(f"总容量: {summary['total_capacity_gb']} GB")
    print(f"已用空间: {summary['total_used_gb']} GB")
    print(f"可用空间: {summary['total_free_gb']} GB")