#include "prague_cc.cpp"

extern "C"
{

    // Constructor
    PragueCC *create_praguecc()
    {
        return new PragueCC();
    }

    // Destructor
    void delete_praguecc(PragueCC *obj)
    {
        delete obj;
    }

    // Now
    time_tp Now(PragueCC *obj)
    {
        return obj->Now();
    }

    // PacketReceived
    bool PacketReceived(PragueCC *obj, time_tp timestamp, time_tp echoed_timestamp)
    {
        return obj->PacketReceived(timestamp, echoed_timestamp);
    }

    // ACKReceived
    count_tp ACKReceived(PragueCC *obj,
                         count_tp packets_received, // echoed_packet counter
                         count_tp packets_CE,       // echoed CE counter
                         count_tp packets_lost,     // echoed lost counter
                         count_tp packets_sent,     // local counter of packets sent up to now, an RTT is reached if remote ACK packets_received+packets_lost
                         bool error_L4S             // receiver found a bleached/error ECN; stop using L4S_id on the sending packets!
                         )                          // how many packets are in flight after the ACKed);
    {
        count_tp inflight = 0; // packets in-flight counter
        bool res = false;
        res = obj->ACKReceived(packets_received, packets_CE, packets_lost, packets_sent, error_L4S, inflight);
        return inflight;
    }

    void DataReceived( // call this when a data packet is received as a receiver and you can identify lost packets
        PragueCC *obj,
        ecn_tp ip_ecn,         // IP.ECN field value
        count_tp packets_lost) // packets skipped; can be optionally -1 to potentially undo a previous cwindow reduction
    {
        obj->DataReceived(ip_ecn, packets_lost);
    }

    void DataReceivedSequence( // call this every time when a data packet with a sequence number is received as a receiver
        PragueCC *obj,
        ecn_tp ip_ecn,          // IP.ECN field value
        count_tp packet_seq_nr) // sequence number of the received packet
    {
        obj->DataReceivedSequence(ip_ecn, packet_seq_nr);
    }

    void ResetCCInfo(PragueCC *obj) // call this when there is a RTO detected
    {
        obj->ResetCCInfo();
    }

    ecn_tp GetTimeInfo( // when the any-app needs to send a packet
        PragueCC *obj,
        time_tp &timestamp,       // Own timestamp to echo by peer
        time_tp &echoed_timestamp // defrosted timestamp echoed to peer
    )
    {
        ecn_tp ip_ecn;
        obj->GetTimeInfo(timestamp, echoed_timestamp, ip_ecn);
        return ip_ecn; // ecn field to be set in the IP header
    }
    size_tp GetCCInfo( // when the sending-app needs to send a packet
        PragueCC *obj,
        rate_tp &pacing_rate,    // rate to pace the packets
        count_tp &packet_window, // the congestion window in number of packets
        count_tp &packet_burst   // number of packets that can be paced at once (<250µs)
    )
    {
        size_tp packet_size;
        obj->GetCCInfo(pacing_rate, packet_window, packet_burst, packet_size);
        return packet_size;
    }

} // End of extern "C"